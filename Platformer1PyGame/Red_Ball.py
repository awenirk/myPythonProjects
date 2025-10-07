from pygame import *
from time import sleep

window = display.set_mode((500, 500))
display.set_caption("Red Ball")
window.fill((255, 200, 200))
clock = time.Clock()

font.init()
mixer.init()
Menu = mixer.Sound('sound/Menu.mp3')
Menu.set_volume(0.8)
Menu.play()

dead = mixer.Sound('sound/dead.mp3')
dead.set_volume(0.8)


DARK_BLUE = (0, 0, 100)
COLOR_4 = (185,132,140)
COLOR_5 = (128,100,145)

class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, w, h):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.isTouch = False
        self.heal = 100

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x -= hero.speed
        if keys[K_a]:
            self.rect.x += hero.speed
# Відступ
    def set_text(self, text, fsize = 12, text_color = (0,0,0)):  # Метод для встановлення тексту
        self.text = text  # Текст для відображення
        self.image = font.Font(None, fsize).render(text, True, text_color)  # Створення зображення з текстом
    def draw(self, shift_x = 0, shift_y = 0):  # Метод для малювання тексту на екрані
        self.fill()  # Заливка прямокутника
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))  # Відображення тексту

class Coin(GameSprite):
    def __init__(self, filename, x, y, speed, w, h):
        GameSprite.__init__(self, filename, x, y, speed, w, h)
        self.counter = 0
        self.isPicked = False

    def animation(self):
        if self.isPicked:
            self.counter += 1
            if 0 <= self.counter < 30:
                self.image = transform.scale(image.load('my_pic/coin_anim1.png'), (self.w, self.h))
            elif 30 <= self.counter < 60:
                self.image = transform.scale(image.load('my_pic/coin_anim2.png'), (self.w, self.h))
            elif 60 <= self.counter < 75:
                self.image = transform.scale(image.load('my_pic/coin_anim3.png'), (self.w, self.h))
            elif 75 <= self.counter < 90:
                self.image = transform.scale(image.load('my_pic/coin_anim4.png'), (self.w, self.h))
            elif 90 <= self.counter < 95:
                self.image = transform.scale(image.load('my_pic/coin_anim5.png'), (self.w, self.h))
            elif 95 <= self.counter < 100:
                self.image = transform.scale(image.load('my_pic/coin_anim6.png'), (self.w, self.h))

            if self.counter == 100:
                coins.remove(self)
                hero.coin_score += 1
                print(f'Coin score: {hero.coin_score}')

class Hero(GameSprite):
    def __init__(self, filename, x, y, speed, w, h):
        GameSprite.__init__(self, filename, x, y, speed, w, h)
        self.coin_score = 0
        self.counter = 0
        self.isJumping = False
        self.jumpCount = 20

    def move(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            self.isJumping = True

        if self.isJumping:
            self.rect.y -= self.jumpCount
            self.jumpCount -= 1
            if self.jumpCount == -26:
                self.isJumping = False
                self.jumpCount = 25

    def animation(self, kind):
        if kind == 'stay':
            self.counter += 1
            if 0 <= self.counter < 10:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 10 <= self.counter < 20:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 20 <= self.counter < 30:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 30 <= self.counter < 40:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))

            if self.counter > 40:
                self.counter = 0

        elif kind == 'go_left':
            self.counter += 1
            if 0 <= self.counter < 10:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 10 <= self.counter < 20:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 20 <= self.counter < 30:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 30 <= self.counter < 40:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 40 <= self.counter < 50:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h))
            elif 50 <= self.counter < 60:
                self.image = transform.scale(image.load('my_pic/pixilart-drawing.png'), (self.w, self.h0))

            if self.counter > 60:
                self.counter = 0

    def check(self, x, y, barellss):
        barell_touch = []
        tmp_area = Rect(x, y, self.w, self.h)
        for barell in barellss:
            barell.reset()
            barell_touch.append(barell.rect.colliderect(tmp_area))
        # print(barell_touch, x, y)
        return True in barell_touch

class Area(GameSprite): 
    def __init__(self, x=0, y=0, width = 10, height = 0, color = None):  # Конструктор класу
        self.rect = Rect(x, y, width, height)  # Створення прямокутника
        self.fill_color = color  # Колір заливки прямокутника
    def color(self, new_color):  # Метод для зміни кольору заливки
        self.fill_color = new_color
    def fill(self):  # Метод для заливки прямокутника кольором
        draw.rect(window, self.fill_color, self.rect)
    def collidepoint(self, x, y):  # Метод для перевірки, чи точка знаходиться всередині прямокутника
        return self.rect.collidepoint(x,y)

class Labe(Area):
    def set_text(self, text, fsize = 12, text_color = (0,0,0)):  # Метод для встановлення тексту та його властивостей
        self.text = text  # Текст для відображення
        self.image = font.Font(None, fsize).render(text, True, text_color)  # Створення зображення з текстом
    def draw(self, shift_x = 0, shift_y = 0):  # Метод для малювання тексту на екрані
        self.fill()  # Заливка прямокутника
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))  # Відображення тексту на екрані

hero = Hero('my_pic/pixilart-drawing.png', 180, 225, 5, 100, 100)

score_text = Labe(395, 0, 105, 35, COLOR_5)  # Створюємо мітку для відображення рахунку.
score_text.set_text("Рахунок: ", 45, DARK_BLUE)  # Встановлюємо текст та параметри мітки.
score_text.draw(0, 0)  # Малюємо мітку на екрані.

score = Labe(425, 35, 50, 25, COLOR_4)  # Створюємо мітку для відображення рахунку.
score.set_text(str(hero.coin_score), 40, DARK_BLUE)  # Встановлюємо текст та параметри мітки.
score.draw(0, 0)  # Малюємо мітку на екрані.

barrel1 = GameSprite('my_pic/Enemy_1.png', 700, 350, 0, 90, 90)
barrel2 = GameSprite('my_pic/Enemy_1.png', 1700, 350, 0, 90, 90)
barrel3 = GameSprite('my_pic/Enemy_1.png', 2100, 350, 0, 90, 90)
barrel4 = GameSprite('my_pic/Enemy_1.png', 2100, 260, 0, 90, 90)
barells = [barrel1, barrel2, barrel3, barrel4]

coin1 = Coin('my_pic/coin_anim4.png', 835, 400, 0, 32, 32)
coin2 = Coin('my_pic/coin_anim4.png', 1635, 400, 0, 32, 32)
coin3 = Coin('my_pic/coin_anim4.png', 2035, 400, 0, 32, 32)
coin4 = Coin('my_pic/coin_anim4.png', -100, 400, 0, 32, 32)
coins = [coin1, coin2, coin3, coin4]

platform = GameSprite('my_pic/Big_bg.png', -640, 350, 10, 1280, 160)

menu_bg = GameSprite('my_pic/bg.jpg', 0, 0, 0, 500, 500)
game_bg = GameSprite('pictures/Menu_bg.png', 0, 0, 0, 500, 500)
btn_play = GameSprite('my_pic/play.png', 200, 200, 0, 100, 100)

btn_menu = GameSprite('my_pic/pause.png', 64, 64, 0, 64, 64)

screen = 'game'
game = True
while game:
    if screen == 'menu':
        menu_bg.reset()
        btn_play.reset()
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if btn_play.rect.collidepoint(x, y):
                    screen = 'game'
    
        display.update()
        clock.tick(60)
    
    if screen == 'game':
        score_text.reset()
        score.reset()
        game_bg.reset()
        platform.reset()
        hero.reset()
        hero.move() 
        btn_menu.reset()
        # update_hero_position(hero, barells)
    
        for barels in barells:
            barels.move()
            barels.reset()
            if hero.rect.colliderect(barels.rect):
                hero.heal -= 5
                print(hero.heal)
        if hero.heal <= 0:
            Menu.stop()
            dead.play()
            sleep(2) 
            game = False
    
        for coin in coins:
            coin.move()
            coin.reset()
            if hero.rect.colliderect(coin.rect):
                coin.isPicked = True
            coin.animation()
    
        keys = key.get_pressed()
        if barels.isTouch:
            if keys[K_a]:
                if not hero.check(hero.rect.x - hero.speed, hero.rect.y, barells):
                    hero.animation('go_right')
                else:
                    hero.animation('stay')
            elif keys[K_d]:
                if not hero.check(hero.rect.x + hero.speed, hero.rect.y, barells):
                    hero.animation('go_left')
            else:
                hero.animation('stay')
    
        # hero.move(barells)
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                # print(x, y)
                if btn_menu.rect.collidepoint(x, y):
                    screen = 'menu'
    
        display.update()
        clock.tick(60)
#Кінець!  =(               Вроді...