from pygame import *
import random

# Картинки
backImg = '1.Images/BackGround.png'
playerImg = '1.Images/Hero1.png'
player1Img = '1.Images/Hero2.png'
emenyImg = '1.Images/Enemy.png'
spiceImg = '1.Images/Spike.png'
spiceImg90 = '1.Images/Spike90.png'
coinImg = '1.Images/Coin.png'
heartImg = '1.Images/Heart.png'
cup_img = '1.Images/Cup.png'
road_img = '1.Images/Road1.png'


# фонова музика
mixer.init()
mixer.music.load('2.Sounds/BackgroundSound.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Звуки гри, та їх гучність
win_sound = mixer.Sound('2.Sounds/win.mp3')
lose_sound = mixer.Sound('2.Sounds/lose.mp3')
win_sound.set_volume(0.35)
lose_sound.set_volume(0.35)

# Шрифт
font.init()
font1 = font.Font('3.Font/minecraft.ttf', 40)

# Класси
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, LorR=None):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.jump_speed = -15
        self.gravity = 0.5
        self.vertical_speed = 0
        self.on_ground = False
        self.rect.centerx = win_width // 2
        self.LorR = LorR
        
        
        self.max_lives = 8
        self.lives = 2  # Починаємо з 2 сердець
        self.invincible = False
        self.invincible_timer = 0
        self.damage_cooldown = 30  # пів секунди невразливості

    def hit(self, damage=1):
        if not self.invincible:
            self.lives -= damage
            self.invincible = True
            return True
        return False

    def heal(self):
        if self.lives < self.max_lives:
            self.lives += 1
            return True
        return False

    def update(self):
        keys = key.get_pressed()
        
        self.rect.centerx = win_width // 2
        
        if keys[K_SPACE] and self.on_ground:
            self.vertical_speed = self.jump_speed
            self.on_ground = False
        
        self.vertical_speed += self.gravity
        self.rect.y += self.vertical_speed
        
        if self.rect.bottom > win_height - 96:
            self.rect.bottom = win_height - 96
            self.vertical_speed = 0
            self.on_ground = True
        
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer > self.damage_cooldown:
                self.invincible = False
                self.invincible_timer = 0
    
    def anim(self):
        if self.LorR == 'left':
            self.image = transform.scale(image.load(player1Img), (128, 128))
        elif self.LorR == 'right':
            self.image = transform.scale(image.load(playerImg), (128, 128))

class Enemy(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed, move_range=128):
        super().__init__(image, x, y, size_x, size_y, speed)
        self.start_x = x
        self.move_range = move_range
        self.direction = 1
        self.base_x = x  # Зберігаємо початкову позицію

    def update(self):
        # Власний рух ворога
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.move_range:
            self.direction *= -1

class Spike(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, damage=1):
        super().__init__(image, x, y, size_x, size_y, 0)
        self.damage = damage

    def update(self, player_speed=0):
        # Рух відносно гравця
        self.rect.x -= player_speed

class Coin(GameSprite):
    def __init__(self, image, x, y, size_x, size_y):
        super().__init__(image, x, y, size_x, size_y, 0)
        self.value = 1
        self.initial_y = y
        self.move_range = 10
        self.move_speed = 1
        self.direction = 1
        self.current_offset = 0

    def update(self, player_speed=0):
        # Анімація вгору-вниз
        self.current_offset += self.move_speed * self.direction
        if abs(self.current_offset) >= self.move_range:
            self.direction *= -1
        self.rect.y = self.initial_y + self.current_offset
        
        # Рух відносно гравця
        self.rect.x -= player_speed

class HealthHeart(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))  # Використовуємо вже завантажене зображення
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0

class Road(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__(image, x, y, size_x, size_y, speed)
        def update(self, player_speed=0):
            # Рух відносно гравця
            self.rect.x -= player_speed
        

# Створюємо віконце
clock = time.Clock()
win_width = 1024
win_height = 576

display.set_caption("Pixel Quest By Awenirk")
win = display.set_mode((win_width, win_height)) # 4.5 x 8   =|=   9 x 16
background = transform.scale(image.load(backImg), (win_width, win_height))

player = Player(playerImg, win_width/2 - 64, win_height/2 - 64,  96, 128,  10, 'right')

cup = GameSprite(cup_img, 7168-512-128, win_height - 384, 256, 256, 0)
# Змінні для гри
FPS = 60
finish = False
run = True

x = 0
roomNum = 0


# Групи обєктів
enemies = sprite.Group()
spikes = sprite.Group()
hearts = sprite.Group()
roads = sprite.Group()
wall = sprite.Group()

heart = HealthHeart(heartImg, -768, win_height - 288-32, 64, 64)
hearts.add(heart)
for x in range(12):
    road = Road(road_img, (x*1024)-4096, win_height-110, 1024, 110, 1)
    roads.add(road)

for s in range(0, 11):
    spike = Spike(spiceImg90, -1024, win_height-(64*s)+64, 64, 64, 10)
    wall.add(spike)
# Створення тексту
game_font = font.Font(None, 70)
win_text = game_font.render('YOU WIN!', True, (0, 255, 0))
lose_text = game_font.render('GAME OVER!', True, (255, 0, 0))

# Головний ігровий цикл
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if not finish:
        win.blit(background, (0, 0))
        
        # Визначаємо швидкість руху об'єктів
        keys = key.get_pressed()
        move_speed = 0
        win.blit(cup.image, cup.rect)
        player.update()
        player.reset()
        player.anim()
        if keys[K_a]:
            player.LorR = 'left'
            move_speed = 5
        if keys[K_d]:
            player.LorR = 'right'
            move_speed = -5
        
        while roomNum != 5:
            room = random.randint(1, 5)
            spawnheart = random.choice([True, False, False, False])
            roomNum += 1
            x += 1024
            # road = Road(road_img, x-1024, win_height-110, 1024, 110, 1)
            # roads.add(road)
            if room == 1:
                print(f"{roomNum}.  {room} - {spawnheart}, 3 spikes")
                if spawnheart == True:
                    heart = HealthHeart(heartImg, x+512-32, win_height - 288-32, 64, 64)
                    hearts.add(heart)
                spike = Spike(spiceImg, x+512-64, win_height-160 + 32, 32, 32)
                spikes.add(spike)
                spike = Spike(spiceImg, x+512-32, win_height-192 + 32, 64, 64)
                spikes.add(spike)
                spike = Spike(spiceImg, x+512+32, win_height-160 + 32, 32, 32)
                spikes.add(spike)
            elif room == 2:
                print(f"{roomNum}.  {room} - {spawnheart}, 2 spikes")
                if spawnheart == True:
                    heart = HealthHeart(heartImg, x+512-32, win_height - 288-32, 64, 64)
                    hearts.add(heart)
                spike = Spike(spiceImg, x+256, win_height-192 + 32, 64, 64)
                spikes.add(spike)
                spike = Spike(spiceImg, x+512+128, win_height-192 + 32, 64, 64)
                spikes.add(spike)
            elif room == 3:
                print(f"{roomNum}.  {room} - {spawnheart}, ptichka")
                if spawnheart == True:
                    heart = HealthHeart(heartImg, x+512-32, win_height - 288-32, 64, 64)
                    hearts.add(heart)
                enemy = Enemy(emenyImg, x+512+256, win_height-192 + 32, 64, 64, 2, 256)
                enemies.add(enemy)
            elif room == 4:
                print(f"{roomNum}.  {room} - True")
                heart = HealthHeart(heartImg, x+512-16, win_height-288-32, 64, 64)
                hearts.add(heart)
            elif room == 5:
                print(f"{roomNum}.  {room} - {spawnheart}, 1+1+1 spikes")
                if spawnheart == True:
                    heart = HealthHeart(heartImg, x+512-32, win_height - 288-32, 64, 64)
                    hearts.add(heart)
                spike = Spike(spiceImg, x+256-16, win_height-160 + 32, 32, 32)
                spikes.add(spike)
                spike = Spike(spiceImg, x+512-32, win_height-192 + 32, 64, 64)
                spikes.add(spike)
                spike = Spike(spiceImg, x+512+256-16, win_height-160 + 32, 32, 32)
                spikes.add(spike)
        
        for enemy in enemies:
            enemy.rect.x += move_speed
            enemy.start_x += move_speed
        enemies.update()
        enemies.draw(win)
        
        for r in roads:
            r.rect.x += move_speed
            r.reset()
            r.update()
        
        for spike in spikes:
            spike.rect.x += move_speed
        for heart in hearts:
            heart.rect.x += move_speed
        for walls in wall:
            walls.rect.x += move_speed
        spikes.draw(win)
        hearts.draw(win)
        wall.draw(win)


        if sprite.spritecollide(player, enemies, False) and player.hit():
            pass  # Можна додати звук удару
        
        # Перевірка зіткнень з шипами
        if sprite.spritecollide(player, spikes, False) and player.hit(spike.damage):
            pass  # Можна додати звук удару
        
        if sprite.spritecollide(player, wall, False) and player.hit(player.lives):
            pass  # Можна додати звук удару
        
        
        # Перевірка підбору сердець
        hearts_collected = sprite.spritecollide(player, hearts, True)
        for heart in hearts_collected:
            player.heal()  # Додаємо життя
        
        # Відображення сердець в інтерфейсі (використовуємо вже існуюче heartImg)
        for i in range(player.lives):
            win.blit(transform.scale(image.load(heartImg), (64, 64)), (10 + i * 25, 50))

        # Рух кубка разом з іншими об'єктами
        cup.rect.x += move_speed
        
        
        
        # Перевірка зіткнення з кубком (перемога)
        if sprite.collide_rect(player, cup):
            win.blit(win_text, (win_width // 2 - 100, win_height // 2))
            win_sound.play()
            display.update()
            time.delay(3000)
            finish = True
            run = False
        
        # Перевірка програшу (коли закінчились життя)
        if player.lives <= 0:
            win.blit(lose_text, (win_width // 2 - 150, win_height // 2))
            lose_sound.play()
            display.update()
            time.delay(3000)
            finish = True
            run = False

    display.update()
    clock.tick(FPS)
