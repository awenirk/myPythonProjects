from pygame import *

# Класи
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, x, y, hor=None, end=None, heal = None):
        super().__init__()
        self.heal = heal
        self.HorW = hor
        if self.HorW == "H": 
            self.start = player_x
        elif self.HorW == "V":
            self.start = player_y
        self.end = end
        self.x = x
        self.y = y
        self.image = transform.scale(image.load(player_image), (x, y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            for wall in walls:
                if sprite.collide_rect(player, wall):
                    self.rect.y += self.speed+10
                    self.heal -= 5
                    print(self.heal)
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            for wall in walls:
                if sprite.collide_rect(player, wall):
                    self.rect.x += self.speed+10
                    self.heal -= 5
                    print(self.heal)
        if keys[K_s] and self.rect.y < win_height:
            self.rect.y += self.speed
            for wall in walls:
                if sprite.collide_rect(player, wall):
                    self.rect.y -= self.speed+10
                    self.heal -= 5
                    print(self.heal)
        if keys[K_d] and self.rect.x < win_height:
            self.rect.x += self.speed
            for wall in walls:
                if sprite.collide_rect(player, wall):
                    self.rect.x -= self.speed+10
                    self.heal -= 5
                    print(self.heal)

class Enemy(GameSprite):
    direction = "right"
    def update(self):
        if self.HorW == "H":
            if self.rect.x <= self.end:
                self.direction = "right"
            if self.rect.x >= self.start:
                self.direction = "left"
        elif self.HorW == "V":
            if self.rect.y <= self.end:
                self.direction = "down"
            if self.rect.y >= self.start:
                self.direction = "up"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, color, wall_width, wall_height, wall_x, wall_y):
        super().__init__()
        self.color = color
        
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Створення вікна
win_width, win_height = 700, 700
window = display.set_mode((win_width, win_height))
display.set_caption("Maze by Awenirk")
background = transform.scale(image.load("Images/Background1.jpg"), (win_width, win_height))


# Ініціалізація музики
mixer.init()
mixer.music.load('gameMusic.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
m_win = mixer.Sound('Money.mp3')
m_lose = mixer.Sound('fail.mp3')
m_win.set_volume(1.0)
m_lose.set_volume(1.0)


# Ігрові змінні
clock = time.Clock()
FPS = 60
a = 50
b = 4
col = (255, 255, 255)
colbg = (0, 50, 50)

# Створення тексту
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (20, 255, 30))
lose = font.render('YOU LOSE!', True, (255, 30, 20))

# Ігрові персонажі
player = Player('Images/Sprites/sprite2.png', 80, 120, 1.6, 26, 26, None, None, 100)
final = GameSprite('Images/Treasure1.png', win_width-2.4*a, win_height-4*a, 0, 50, 50)


# монстрикb і лабіринт
monsters = [
    Enemy('Images/Sprites/sprite5.png', 11*a+5, 3*a+5, 1, 44, 44, "H", 10*a),
    Enemy('Images/Sprites/sprite8.png', 4*a+5, 7*a+5, 1, 44, 44, "V", 4*a),
    Enemy('Images/Sprites/sprite10.png', 4*a+5, 11*a+5, 1, 44, 44, "H", 2*a),
    Enemy('Images/Sprites/sprite11.png', 6*a+5, 12*a+5, 1, 44, 44, "V", 10*a)
]

walls = [
    Wall(colbg, 10*a, a, 4*a, 0),
    Wall(colbg, a, 7*a, 13*a, 0),
    Wall(colbg, a, 8*a, 0, 6*a),
    Wall(colbg, 10*a, a, 0, 13*a),
    
    Wall(col, 14*a, b, 0, 0),
    Wall(col, 9*a+b, b, 4*a, a), #1ряд
    Wall(col, a+b, b, 6*a, 2*a), #2ряд
    Wall(col, 2*a+b, b, 8*a, 2*a),
    Wall(col, a+b, b, 11*a, 2*a),
    Wall(col, a+b, b, 4*a, 3*a), #3ряд
    Wall(col, 2*a+b, b, 9*a, 3*a),
    Wall(col, a+b, b, 4*a, 4*a), #4ряд
    Wall(col, a+b, b, 6*a, 4*a),
    Wall(col, a+b, b, 8*a, 4*a),
    Wall(col, 2*a+b, b, 5*a, 5*a), #5ряд
    Wall(col, a+b, b, 8*a, 5*a),
    Wall(col, a+b, b, 10*a, 5*a),
    Wall(col, 4*a+b, b, 0, 6*a), #6ряд
    Wall(col, a+b, b, 7*a, 6*a),
    Wall(col, 3*a+b, b, 9*a, 6*a),
    Wall(col, 2*a+b, b, 2*a, 7*a), #7ряд
    Wall(col, a+b, b, 5*a, 7*a),
    Wall(col, a+b, b, 7*a, 7*a),
    Wall(col, 5*a+b, b, 9*a, 7*a),
    Wall(col, a+b, b, 2*a, 8*a), #8ряд
    Wall(col, 5*a+b, b, 4*a, 8*a),
    Wall(col, 2*a+b, b, a, 9*a), #9ряд
    Wall(col, 4*a+b, b, 5*a, 9*a),
    Wall(col, a+b, b, 2*a, 10*a), #10ряд
    Wall(col, 5*a+b, b, 5*a, 10*a),
    Wall(col, a+b, b, 3*a, 11*a), #11ряд
    Wall(col, a+b, b, 5*a, 11*a),
    Wall(col, 3*a+b, b, 7*a, 11*a),
    Wall(col, 2*a+b, b, 2*a, 12*a), #12ряд
    Wall(col, 2*a+b, b, 7*a, 12*a),
    Wall(col, 9*a+b, b, a, 13*a), #13ряд
    Wall(col, 14*a, b, 0, 14*a-b),
    
    Wall(col, b, 14*a, 0, 0),
    Wall(col, b, 7*a+b, a, 6*a), #1стовпчик
    Wall(col, b, 2*a+b, 2*a, 10*a), #2стовпчик
    Wall(col, b, a+b, 3*a, 8*a), #3стовпчик
    Wall(col, b, a+b, 3*a, 10*a),
    Wall(col, b, 3*a+b, 4*a, 0), #4стовпчик
    Wall(col, b, 3*a+b, 4*a, 4*a),
    Wall(col, b, 3*a+b, 4*a, 8*a),
    Wall(col, b, a+b, 5*a, 2*a), #5стовпчик
    Wall(col, b, a+b, 5*a, 4*a),
    Wall(col, b, a+b, 5*a, 6*a),
    Wall(col, b, a+b, 5*a, 8*a),
    Wall(col, b, 2*a+b, 5*a, 11*a),
    Wall(col, b, 3*a+b, 6*a, a), #6стовпчик
    Wall(col, b, 2*a+b, 6*a, 5*a),
    Wall(col, b, a+b, 6*a, 11*a),
    Wall(col, b, a+b, 7*a, 3*a), #7стовпчик
    Wall(col, b, a+b, 7*a, 5*a),
    Wall(col, b, a+b, 7*a, 7*a),
    Wall(col, b, a+b, 7*a, 11*a),
    Wall(col, b, 2*a+b, 8*a, a), #8стовпчик
    Wall(col, b, a+b, 8*a, 5*a),
    Wall(col, b, 2*a+b, 9*a, 3*a), #9стовпчик
    Wall(col, b, a+b, 9*a, 7*a),
    Wall(col, b, 2*a+b, 10*a, 3*a), #10стовпчик
    Wall(col, b, 3*a+b, 10*a, 7*a),
    Wall(col, b, 3*a+b, 10*a, 11*a),
    Wall(col, b, a+b, 11*a, a), #11стовпчик
    Wall(col, b, a+b, 11*a, 4*a),
    Wall(col, b, 4*a+b, 12*a, 2*a), #12стовпчик
    Wall(col, b, 6*a+b, 13*a, a), #13стовпчик
    Wall(col, b, 14*a, 14*a-b, 0),
]


# Ігровий цикл
finish = False
GAME = True
win_sound_played = False
lose_sound_played = False

while GAME:
    for e in event.get():
        if e.type == QUIT:
            GAME = False

    if not finish:
        window.blit(background, (0, 0))
        
        player.update()
        player.reset()
        
        for m in monsters:
            m.update()
            m.reset()
        
        final.reset()
        
        # Малюємо стіни
        for wall in walls:
            wall.draw_wall()
        
        # Перевіряємо зіткнення з фінальним об'єктом
        if sprite.collide_rect(player, final):
            window.blit(win, (200, 300))
            if not win_sound_played:
                m_win.play()
                win_sound_played = True
            finish = True
        for m in monsters:
            if sprite.collide_rect(player, m):
                window.blit(lose, (200, 300))
                if not lose_sound_played:
                    m_lose.play()
                    lose_sound_played = True
                finish = True

    else:
        mixer.music.stop()
        display.update()
        time.delay(3000)
        GAME = False

    display.update()
    clock.tick(FPS)

quit()
