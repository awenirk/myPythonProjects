from pygame import *
import random

# Звуки
mixer.init()
mixer.music.load('Sounds/space.mp3')
mixer.music.play()
fire_sound = mixer.Sound('Sounds/fire.ogg')

# Змінюємо гучність музики
mixer.music.set_volume(0.2)
fire_sound.set_volume(0.35)

# нам потрібні такі картинки
img_back = "Images/space.jpg"  # фон гри
img_hero = "Images/player.png"  # герой
img_bullet = "Images/bullet.png"  # зображення кулі
img_enemy = "Images/ufo.png"  # зображення ворога
img_health = "Health.png"
font.init()
font1 = font.Font('Fonts/Comfortaa-Regular.ttf', 36)
font_bold = font.Font(None, 36)
font_light = font.Font(None, 36)
font_big = font.Font(None, 210)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 128:
            self.rect.x += self.speed

    def fire(self):
        global bullets_count
        if bullets_count > 0:  # Перевіряємо наявність куль
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
            bullets.add(bullet)
            bullets_count -= 1  # Зменшуємо кількість куль

class Enemy(GameSprite):
    def update(self):
        global lives
        self.rect.y += self.speed
        if self.rect.y >= win_height - 128:  # Змінюємо умову, враховуючи розмір спрайту
            self.rect.x = random.randint(0, win_width - 128)
            self.rect.y = -40
            lives -= 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


# створюємо віконце
win_width = 1024
win_height = 576
display.set_caption("Shooter By Awenirk")
window = display.set_mode((win_width, win_height)) # 4.5 x 8   ==   9 x 16
background = transform.scale(image.load(img_back), (win_width, win_height))

# Додаємо створення clock
clock = time.Clock()


# Додаємо нові змінні після інших початкових змінних
bullets_count = 1  # Початкова кількість куль
reload_timer = 0   # Таймер для перезарядки

# Додаємо функцію перевірки перекриття перед створенням спрайтів
def is_overlapping(new_x, monsters):
    for monster in monsters:
        if abs(monster.rect.x - new_x) < 128:  # Перевіряємо відстань між монстрами
            return True
    return False

# Створюємо спрайти
ship = Player(img_hero, win_width/2 - 64, win_height - 128,  128, 128,  10)
bullets = sprite.Group()
monsters = sprite.Group()


FPS = 60
score = 0  # збито кораблів
lives = 3  # кількість життів
monster_count = 0  # лічильник створених монстрів
finish = False
run = True

# Створюємо 2 монстри на початку
for i in range(3):
    attempts = 0
    while attempts < 10:
        new_x = random.randint(0, win_width - 128)
        if not is_overlapping(new_x, monsters):
            monster = Enemy(img_enemy, new_x,  -40,  128, 128, 1.5)
            monsters.add(monster)
            monster_count += 1
            break
        attempts += 1


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullets_count > 0:  # Стріляємо тільки якщо є кулі
                    ship.fire()
                    fire_sound.play()

    # Перевіряємо умову програшу
    if not finish:
        window.blit(background, (0, 0))

        # Продовжуємо гру тільки якщо lives > 0
        if lives <= 0:
            finish = True
            window.blit(background, (0, 0))
            lose = font_big.render("GAME OVER", True, (255, 0, 0))
            window.blit(lose, (win_width//2 - lose.get_width()//2, win_height//2))
        else:
            monsters.update()
            monsters.draw(window)

            bullets.update()
            bullets.draw(window)

            ship.update()
            ship.reset()

            # Оновлення таймера куль
            reload_timer += 1
            if reload_timer >= 45:
                if bullets_count < 5:
                    bullets_count += 1
                reload_timer = 0

            # Перевірка колізій та інша логіка гри
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                monster_count -= 1
                if monster_count < 3:
                    attempts = 0
                    while attempts < 10:
                        new_x = random.randint(0, win_width - 128)
                        if not is_overlapping(new_x, monsters):
                            monster = Enemy(img_enemy,
                                         new_x,
                                         -40,
                                         128, 128,
                                         1.5)
                            monsters.add(monster)
                            monster_count += 1
                            break
                        attempts += 1

            # Відображення тексту
            text_score = font_bold.render("Рахунок: " + str(score), True, (255, 255, 255))
            window.blit(text_score, (10, 20))
            text_lives = font_light.render("Життя: " + str(lives), 1, (255, 255, 255))
            window.blit(text_lives, (10, 50))
            text_bullets = font_light.render("Кулі: " + str(bullets_count), 1, (255, 255, 255))
            window.blit(text_bullets, (10, 80))

            # Перевірка перемоги
            if score >= 25:
                finish = True
                window.blit(background, (0, 0))
                win_text = font_big.render("YOU WIN!", True, (0, 255, 0))
                # Розміщуємо текст точно по центру
                text_rect = win_text.get_rect(center=(win_width/2, win_height/2))
                window.blit(win_text, text_rect)

    display.update()
    clock.tick(FPS)
