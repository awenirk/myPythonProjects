import pygame  # Імпорт модуля pygame для створення графічного інтерфейсу
from random import randint  # Імпорт функції randint з модуля random для генерації випадкових чисел
import time
from time import sleep  # Імпорт модуля time для роботи з часом
# Відступ)
pygame.init()  # Ініціалізація модуля pygame
FILL_COLOR = (2,49,94) # Визначення кольору black
nw = pygame.display.set_mode((500, 500))  # Створення екрану гри
nw.fill(FILL_COLOR)  # Заповнення екрану чорним кольором
clock = pygame.time.Clock()  # Створення об'єкту для керування часом гри
# Відступ)
class Area():  # Визначення класу Area для створення об'єктів зі свійствами прямокутників
    def __init__(self, x=0, y=0, width = 10, height = 0, color = None):  # Конструктор класу
        self.rect = pygame.Rect(x, y, width, height)  # Створення прямокутника
        self.fill_color = color  # Колір заливки прямокутника
    def color(self, new_color):  # Метод для зміни кольору заливки
        self.fill_color = new_color
    def fill(self):  # Метод для заливки прямокутника кольором
        pygame.draw.rect(nw, self.fill_color, self.rect)
    def outline(self):  # Метод для малювання контуру прямокутника
        pygame.draw.rect(nw, self.fill_color, self.thinckness)
    def collidepoint(self, x, y):  # Метод для перевірки, чи точка знаходиться всередині прямокутника
        return self.rect.collidepoint(x,y)
# Відступ)
class Labe(Area):  # Визначення класу Labe для створення об'єктів для відображення тексту
    def set_text(self, text, fsize = 12, text_color = (0,0,0)):  # Метод для встановлення тексту та його властивостей
        self.text = text  # Текст для відображення
        self.image = pygame.font.Font(None, fsize).render(text, True, text_color)  # Створення зображення з текстом
    def draw(self, shift_x = 0, shift_y = 0):  # Метод для малювання тексту на екрані
        self.fill()  # Заливка прямокутника
        nw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))  # Відображення тексту на екрані
# Відступ)
RED = (255, 0, 0)  # Визначення кольору RED
GREEN = (0, 255, 51)  # Визначення кольору GREEN
BlUE = (0, 0, 255)  # Визначення кольору BlUE
ORANGE = (255, 123, 0)  # Визначення кольору ORANGE
WHITE = (255, 255, 255)  # Визначення кольору WHITE
YELLOW = (255, 255, 0)  # Визначення кольору YELLOW
LIGHT_GREEN = (200, 255, 200)  # Визначення кольору LIGHT_GREEN
LIGHT_RED = (250, 128, 114)  # Визначення кольору LIGHT_RED
BLACK = (0, 0, 0)  # Визначення кольору BLACK
DARK_BLUE = (0, 0, 100)  # Визначення кольору DARK_BLUE
LIGHT_BLUE = (80, 80, 255)  # Визначення кольору LIGHT_BLUE
COLOR_1 = (2,49,94)  # Визначення кольору COLOR_1
COLOR_2 = (0,69,126)  # Визначення кольору COLOR_2
COLOR_3 = (47,112,175)  # Визначення кольору COLOR_3
COLOR_4 = (185,132,140)  # Визначення кольору COLOR_4
COLOR_5 = (128,100,145)  # Визначення кольору COLOR_5
# Відступ)
cards = list()  # Створення порожнього списку cards
num_cards = 4  # Кількість карт
x = 70  # Початкова координата x
# Відступ)
start_time = time.time()  # Отримання часу початку виконання програми
cur_time = start_time  # Початковий час
# Відступ)
time_text = Labe(0, 0, 90, 70, COLOR_2)  # Створюємо мітку для відображення часу.
time_text.set_text("Час: ", 40, DARK_BLUE)  # Встановлюємо текст та параметри мітки.
time_text.draw(20, 20)  # Малюємо мітку на екрані.
# Відступ
timer = Labe(90, 20, 40, 25, COLOR_3)  # Створюємо мітку для відображення таймера.
timer.set_text("0", 40, DARK_BLUE)  # Встановлюємо текст та параметри мітки.
timer.draw(0, 0)  # Малюємо мітку на екрані.
# Відступ)
score_text = Labe(395, 0, 105, 35, COLOR_5)  # Створюємо мітку для відображення рахунку.
score_text.set_text("Рахунок", 45, DARK_BLUE)  # Встановлюємо текст та параметри мітки.
score_text.draw(0, 0)  # Малюємо мітку на екрані.
# Відступ)
score = Labe(425, 35, 50, 25, COLOR_4)  # Створюємо мітку для відображення рахунку.
score.set_text("0", 40, DARK_BLUE)  # Встановлюємо текст та параметри мітки.
score.draw(0, 0)  # Малюємо мітку на екрані.
# Відступ)
for i in range(num_cards):  # Генеруємо картки.
    new_cards = Labe(x, 170, 70, 100, YELLOW)  # Створюємо нову картку.
    new_cards.set_text("CLICK", 26)  # Встановлюємо текст та параметри мітки на картці.
    cards.append(new_cards)  # Додаєм картку до списку карт.
    # Відступ)
    x += 100 # Збільшуємо значення x для розташування наступної картки.
# Відступ)
wait = 0 # Ініціалізуємо змінну очікування кліку.
point = 0 # Ініціалізуємо змінну рахунку.
# Відступ)
while True: # Головний цикл гри.
    if wait == 0: # Перевіряємо чи відбувається очікування кліку.
        wait = 20 # Встановлюємо час очікування.
        CLICK = randint(1, num_cards) # Генеруємо випадковий номер картки для кліку.
        for i in range(num_cards): # Перебираємо всі картки.
            cards[i].color(COLOR_3) # Встановлюємо колір картки.
            if (i + 1) == CLICK: # Перевіряємо, чи поточна картка співпадає з випадковою.
                cards[i].draw(10, 40) # Малюємо картку з відступом.
            else:
                cards[i].fill() # Заливаємо картку стандартним кольором.
    else:
        wait -= 1 # Зменшуємо час очікування.
    # Відступ)
    for event in pygame.event.get():  # Обробляємо події.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Перевіряємо клік мишею.
            x, y = event.pos  # Отримуємо координати кліку.
            for i in range(num_cards):  # Перебираємо всі картки.
                if cards[i].collidepoint(x, y):  # Перевіряємо колізію кліку з карткою.
                    if i + 1 == CLICK:  # Перевіряємо чи клікнуто на вірну картку.
                        cards[i].color(GREEN)  # Змінюємо колір картки на зелений.
                        point += 1  # Збільшуємо рахунок.
                    else:
                        cards[i].color(RED)  # Змінюємо колір картки на червоний.
                        point -= 1  # Зменшуємо рахунок.
                    cards[i].fill()  # Заливаємо картку новим кольором.
                    score.set_text(str(point), 40, DARK_BLUE)  # Оновлюємо текст рахунку.
                    score.draw(0, 0)  # Малюємо мітку рахунку.
    # Відступ)
    new_time = time.time()  # Отримуємо новий час.
    if int(new_time) - int(cur_time) == 1:  # Перевіряємо чи пройшла одна секунда.
        timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)  # Оновлюємо текст таймера.
        timer.draw(0, 0)  # Малюємо мітку таймера.
        cur_time = new_time  # Оновлюємо поточний час.
    # Відступ)
    if new_time - start_time >= 30:  # Перевіряємо чи вичерпано час гри.
        win = Labe(0, 0, 500, 500, COLOR_3)  # Створюємо мітку для відображення виграшу.
        win.set_text("Час вичерпано!!!", 60, BLACK)  # Встановлюємо текст та параметри мітки.
        win.draw(110, 110)  # Малюємо мітку на екрані.
        pygame.display.update()  # Оновлюємо відображення.
        break  # Завершуємо гру.
    # Відступ)
    if point >= 7:  # Перевіряємо чи досягнуто необхідний рахунок для перемоги.
        win = Labe(0, 0, 500, 500, COLOR_1)  # Створюємо мітку для відображення перемоги.
        win.set_text("Ти переміг!!!", 60, WHITE)  # Встановлюємо текст та параметри мітки.
        win.draw(140, 180)  # Малюємо мітку на екрані.
        resul_time = Labe(90, 230, 315, 40,     COLOR_5)  # Створюємо мітку для відображення часу гри.
        resul_time.set_text("Час проходження: " + str(int(new_time - start_time)) + " Секунд", 40, COLOR_4)  # Встановлюємо текст та параметри мітки.
        resul_time.draw(0, 0)  # Малюємо мітку на екрані.
        pygame.display.update()  # Оновлюємо відображення.
        break  # Завершуємо гру.
    # Відступ)
    pygame.display.update()  # Оновлюємо відображення.
    clock.tick(40)  # Обмежуємо кількість кадрів на секунду.
sleep(4)
# Кінець