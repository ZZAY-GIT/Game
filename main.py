import random
import sys
import pygame
import os


pygame.init()
pygame.mixer.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
collision_sound = pygame.mixer.Sound("data\\123.mp3")


# класс мячика
class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.image.load('data\\ball.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 8
        self.vy = -8

    def update(self, bricks):
        if 0 <= self.rect.x + self.vx <= width - self.radius:
            self.rect = self.rect.move(self.vx, self.vy)
        else:
            self.vx = -self.vx
        if 0 >= self.rect.y - self.radius:
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, paddle):
            self.vy = -self.vy
            for i in paddle:
                paddle_center = i.rect.x + (i.rect.width / 2)
                ball_center = self.rect.x + self.radius / 2
                offset = (ball_center - paddle_center) / (i.rect.width / 2)

                self.vx = offset * 5
        if pygame.sprite.spritecollide(self, bricks, True):
            collision_sound.play()
            self.vy = -self.vy


# класс платформы
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data\\paddle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def update(self, direction):
        if direction == 'right':
            if self.rect.x + 10 <= width - self.width:
                self.rect = self.rect.move(10, 0)
        else:
            if self.rect.x - 10 >= 0:
                self.rect = self.rect.move(-10, 0)


# класс кирпича
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(all_sprites)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height


# создание кирпичей
def create_bricks(level, bricks):
    images = ['data\\brick1.png', 'data\\brick2.png', 'data\\brick3.png', 'data\\brick4.png']
    bricks_coords = []
    x_coords = list(range(50, 750, 50))
    y_coords = list(range(50, 170, 30))
    for i in range(31 + (level + 1) * 5):
        x_pos = random.choice(x_coords)
        y_pos = random.choice(y_coords)
        while (x_pos, y_pos) in bricks_coords:
            x_pos = random.choice(x_coords)
            y_pos = random.choice(y_coords)
        bricks_coords.append((x_pos, y_pos))
        bricks.add(Brick(x_pos, y_pos, 50, 30, random.choice(images)))


class Button:
    def __init__(self, text, font, pos, color, changed_color):
        self.text = text
        self.font = font
        self.x, self.y = pos
        self.color, self.changed_color = color, changed_color
        self.result_text = self.font.render(self.text, True, self.color)
        self.rect = self.result_text.get_rect(center=(self.x, self.y))
        self.text_of_rect = self.result_text.get_rect(center=(self.x, self.y))

    def check(self, pos):
        x, y = pos
        if self.rect.left <= x <= self.rect.right and self.rect.top <= y <= self.rect.bottom:
            return True
        return False

    def change(self, pos):
        x, y = pos
        if self.rect.left <= x <= self.rect.right and self.rect.top <= y <= self.rect.bottom:
            self.result_text = self.font.render(self.text, True, self.changed_color)
        else:
            self.result_text = self.font.render(self.text, True, self.color)


def play(level):
    pygame.display.set_caption("Арканоид")
    running = True
    moving = False
    bricks = pygame.sprite.Group()
    create_bricks(level, bricks)
    all_sprites.add(ball, bricks, paddle)
    while running:
        screen.blit(pygame.image.load("data\\fon_3.jpg"), (0, 0))
        font = pygame.font.Font(None, 50)
        text1 = font.render('', True, (255, 255, 255))
        screen.blit(text1, (25, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

        all_sprites.draw(screen)
        ball.update(bricks)
        # передвижение платформы клавишами

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.update('left')
        if keys[pygame.K_RIGHT]:
            paddle.update('right')

        # передвижение платформы мышью
        if moving:
            for i in paddle:
                mouse_x, _ = pygame.mouse.get_pos()
                i.rect.x = mouse_x - i.width // 2
        pygame.display.flip()
    pygame.quit()
    sys.exit()


def level_select():
    global passed_levels
    pygame.display.set_caption("Выбор уровня")
    running = True
    buttons = ['Уровень 1', 'Уровень 2', 'Уровень 3', 'Уровень 4', 'Уровень 5']
    while running:
        color = 'white'
        color_changed = 'green'
        pos = pygame.mouse.get_pos()
        screen.blit(pygame.image.load('data\\fon_2.jpg'), (0, 0))
        button1 = Button(buttons[0], pygame.font.Font(None, 50), (200 + 200 * 0, 200), color, color_changed)
        button1.change(pos)
        screen.blit(button1.result_text, button1.text_of_rect)
        if passed_levels == 0:
            color = 'red'
            color_changed = color
        button2 = Button(buttons[1], pygame.font.Font(None, 50), (200 + 200 * 1, 200), color, color_changed)
        button2.change(pos)
        screen.blit(button2.result_text, button2.text_of_rect)
        if passed_levels == 1:
            color = 'red'
            color_changed = color
        button3 = Button(buttons[2], pygame.font.Font(None, 50), (200 + 200 * 2, 200), color, color_changed)
        button3.change(pos)
        screen.blit(button3.result_text, button3.text_of_rect)
        if passed_levels == 2:
            color = 'red'
            color_changed = color
        button4 = Button(buttons[3], pygame.font.Font(None, 50), (300 + 200 * 0, 300), color, color_changed)
        button4.change(pos)
        screen.blit(button4.result_text, button4.text_of_rect)
        if passed_levels == 3:
            color = 'red'
            color_changed = color
        button5 = Button(buttons[4], pygame.font.Font(None, 50), (300 + 200 * 1, 300), color, color_changed)
        button5.change(pos)
        screen.blit(button5.result_text, button5.text_of_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check(pos):
                    play(0)
                if button2.check(pos):
                    if passed_levels > 0:
                        play(1)
                if button3.check(pos):
                    if passed_levels > 1:
                        play(2)
                if button4.check(pos):
                    if passed_levels > 2:
                        play(3)
                if button5.check(pos):
                    if passed_levels > 3:
                        play(4)
        pygame.display.flip()


def first_open():
    pygame.display.set_caption("Информационное окно")
    running = True
    while running:
        screen.blit(pygame.image.load("data\\fon_2.jpg"), (0, 0))
        font = pygame.font.Font(None, 50)
        text1 = font.render('Добро пожаловать в нашу игру "Арканоид!"', True, (255, 255, 255))
        screen.blit(text1, (25, 100))
        text2 = font.render('Управлять платформой можно с помощью ', True, (255, 255, 255))
        screen.blit(text2, (35, 200))
        text3 = font.render('клавиш "A" и "D, а также с помощью мышки', True, (255, 255, 255))
        screen.blit(text3, (25, 300))
        text4 = font.render('Нажимай "ОК" и начинай играть!', True, (255, 255, 255))
        screen.blit(text4, (130, 450))
        ok_b = Button("ОК", pygame.font.Font(None, 75), (400, 550), "white", "green")
        pos = pygame.mouse.get_pos()
        ok_b.change(pos)
        screen.blit(ok_b.result_text, ok_b.text_of_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ok_b.check(pos):
                    main_menu()
                    running = False
        pygame.display.flip()


def main_menu():
    pygame.display.set_caption("Главное меню")
    running = True
    while running:
        screen.blit(pygame.image.load("data\\fon_2.jpg"), (0, 0))
        play_b = Button("ИГРАТЬ", pygame.font.Font(None, 75), (200, 300), "white", "green")
        exit_b = Button("ВЫЙТИ", pygame.font.Font(None, 75), (600, 300), "white", "red")
        level_choose_b = Button('ВЫБОР УРОВНЯ', pygame.font.Font(None, 75), (400, 450), 'white', 'blue')
        text_of_menu = pygame.font.Font(None, 100).render("АРКАНОИД", True, "white")
        rect_of_menu = text_of_menu.get_rect(center=(400, 100))
        screen.blit(text_of_menu, rect_of_menu)
        pos = pygame.mouse.get_pos()
        play_b.change(pos)
        screen.blit(play_b.result_text, play_b.text_of_rect)
        exit_b.change(pos)
        screen.blit(exit_b.result_text, exit_b.text_of_rect)
        level_choose_b.change(pos)
        screen.blit(level_choose_b.result_text, level_choose_b.text_of_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_b.check(pos):
                    play(passed_levels)
                if exit_b.check(pos):
                    running = False
                if level_choose_b.check(pos):
                    level_select()
        pygame.display.flip()
    pygame.quit()
    sys.exit()


# создаём шарик, платформу и кирпичи
paddle = pygame.sprite.Group()
ball = Ball(10, 400, 280)
paddle.add(Paddle(350, 510, 150, 30))
# Добавляем спрайты
passed_levels = 2
last_level = 0
clock = pygame.time.Clock()
if not os.path.exists('data\\user.txt'):
    file = open('data\\user.txt', 'w')
    file.write('logged')
    file.close()
else:
    main_menu()
