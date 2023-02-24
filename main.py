import random
import sys
import pygame
import os

pygame.init()
pygame.mixer.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
collision_sound = pygame.mixer.Sound("data\\bomp.mp3")
gameOverSound = pygame.mixer.Sound('data\\gameover.mp3')
winSound = pygame.mixer.Sound('data\\win.mp3')


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

    # изменение направления мячика
    def update(self, bricks):
        if 0 <= self.rect.x + self.vx <= width - self.radius:
            self.rect = self.rect.move(self.vx, self.vy)
        else:
            self.vx = -self.vx
        if not (0 <= self.rect.y + self.vy <= height - self.radius):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, paddle):
            self.vy = -self.vy
            for i in paddle:
                paddle_center = i.rect.x + (i.rect.width / 2)
                ball_center = self.rect.x + self.radius / 2
                offset = (ball_center - paddle_center) / (i.rect.width / 2)
                self.vx = offset * 5


# класс платформы
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, wid, height):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data\\paddle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = wid
        self.height = height

    # передвижение платформы
    def update(self, direction):
        if direction == 'right':
            if self.rect.x + 10 <= width - self.width:
                self.rect = self.rect.move(10, 0)
        else:
            if self.rect.x - 10 >= 0:
                self.rect = self.rect.move(-10, 0)

    def get_pos(self):
        return self.rect.x, self.rect.y


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


# класс кнопок
class Button:
    def __init__(self, text, font, pos, color, changed_color):
        self.text = text
        self.font = font
        self.x, self.y = pos
        self.color, self.changed_color = color, changed_color
        self.result_text = self.font.render(self.text, True, self.color)
        self.rect = self.result_text.get_rect(center=(self.x, self.y))
        self.text_of_rect = self.result_text.get_rect(center=(self.x, self.y))

    # проверка при наведении на кнопку
    def check(self, pos):
        x, y = pos
        if self.rect.left <= x <= self.rect.right and self.rect.top <= y <= self.rect.bottom:
            return True
        return False

    # изменение цвета кнопки, если оно требуется
    def change(self, pos):
        x, y = pos
        if self.rect.left <= x <= self.rect.right and self.rect.top <= y <= self.rect.bottom:
            self.result_text = self.font.render(self.text, True, self.changed_color)
        else:
            self.result_text = self.font.render(self.text, True, self.color)


# класс данных
class Info:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.current_level = 0
        self.passed_level = 0
        self.last_score = 0
        self.paused = False


# создание кирпичей
def create_bricks(level, bricks):
    images = ['data\\brick1.png', 'data\\brick2.png', 'data\\brick3.png', 'data\\brick4.png']
    bricks_coords = []
    x_coords = list(range(50, 750, 50))
    y_coords = list(range(50, 170, 30))
    # for i in range(31 + (level + 1) * 5):
    for i in range(1):
        x_pos = random.choice(x_coords)
        y_pos = random.choice(y_coords)
        while (x_pos, y_pos) in bricks_coords:
            x_pos = random.choice(x_coords)
            y_pos = random.choice(y_coords)
        bricks_coords.append((x_pos, y_pos))
        bricks.add(Brick(x_pos, y_pos, 50, 30, random.choice(images)))


# меню проигрыша
def restart_menu():
    pygame.display.set_caption("Вы проиграли!")
    running = True
    while running:
        screen.blit(pygame.image.load("data\\fon_2.jpg"), (0, 0))
        font = pygame.font.Font(None, 75)
        text_high_score = font.render(f'Лучший счёт: {Info.high_score}', True, (255, 255, 255))
        screen.blit(text_high_score, (200, 350))
        text_score = font.render(f'Текущий счёт: {Info.score}', True, (255, 255, 255))
        screen.blit(text_score, (200, 300))
        text1 = font.render('Вы проиграли!', True, (220, 100, 100))
        screen.blit(text1, (200, 100))
        pos = pygame.mouse.get_pos()
        restart_b = Button("Перезапустить", pygame.font.Font(None, 75), (600, 550), "white", "green")
        restart_b.change(pos)
        screen.blit(restart_b.result_text, restart_b.text_of_rect)
        main_menu_b = Button("Главное меню", pygame.font.Font(None, 75), (200, 550), "white", "green")
        main_menu_b.change(pos)
        screen.blit(main_menu_b.result_text, main_menu_b.text_of_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_b.check(pos):
                    Info.score = 0
                    play(Info.current_level)
                    running = False
                if main_menu_b.check(pos):
                    Info.score = 0
                    main_menu()
                    running = False
        pygame.display.flip()


# окно игры
def play(level):
    pygame.display.set_caption("Арканоид")
    running = True
    moving = False
    bricks = pygame.sprite.Group()
    create_bricks(level, bricks)
    all_sprites.add(ball, bricks, paddle)
    count_of_bricks = len(bricks)
    while running:
        screen.blit(pygame.image.load("data\\fon_3.jpg"), (0, 0))
        font = pygame.font.Font(None, 40)
        text1 = font.render(f'Уровень: {Info.current_level + 1}', True, (255, 255, 255))
        screen.blit(text1, (0, 0))
        score_text = font.render(f'Счёт: {Info.score}', True, (255, 255, 255))
        screen.blit(score_text, (650, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False
            if event.type == pygame.KEYDOWN and event.key == 27:
                pause_game()
        all_sprites.draw(screen)
        if Info.score > Info.high_score:
            Info.high_score = Info.score
        ball.update(bricks)
        if pygame.sprite.spritecollide(ball, bricks, True):
            collision_sound.play()
            Info.score = Info.last_score + (count_of_bricks - len(bricks))
            with open('data\\user.txt', 'r+') as data:
                data.write('logged\n')
                data.write(f'{Info.score}\n')
                data.write(f'{Info.current_level}\n')
                data.write(f'{Info.passed_levels}\n')
                data.write(f'{Info.high_score}\n')
            ball.vy = -ball.vy

        if ball.rect.y + 10 >= 520:
            gameOverSound.play()
            all_sprites.remove(bricks)
            bricks.clear(screen, screen)
            ball.rect.y, ball.rect.x = 400, 280
            ball.vx, ball.vy = 8, -8
            with open('data\\user.txt', 'r+') as data:
                data.write('logged\n')
                data.write(f'0\n')
                data.write(f'{Info.current_level}\n')
                data.write(f'{Info.passed_levels}\n')
                data.write(f'{Info.high_score}\n')
            running = False
            restart_menu()

        # передвижение платформы клавишами
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.update('left')
        if keys[pygame.K_RIGHT]:
            paddle.update('right')
        if len(bricks) == 0:
            winSound.play()
            running = False
            win_menu()
        # передвижение платформы мышью
        if moving:
            for i in paddle:
                mouse_x, _ = pygame.mouse.get_pos()
                i.rect.x = mouse_x - i.width // 2
        pygame.display.flip()
    pygame.quit()
    sys.exit()


# меню выигрыша
def win_menu():
    pygame.display.set_caption("Победа!!!")
    running = True
    while running:
        screen.blit(pygame.image.load("data\\fon_2.jpg"), (0, 0))
        font = pygame.font.Font(None, 100)
        text1 = font.render('Вы победили!!!', True, 'green')
        screen.blit(text1, (150, 200))
        pos = pygame.mouse.get_pos()
        if Info.current_level != 4:
            next_lvl_b = Button("Следующий уровень", pygame.font.Font(None, 50), (600, 550), "white", "green")
            next_lvl_b.change(pos)
            screen.blit(next_lvl_b.result_text, next_lvl_b.text_of_rect)
            main_menu_b = Button("Главное меню", pygame.font.Font(None, 50), (200, 550), "white", "green")
            main_menu_b.change(pos)
            screen.blit(main_menu_b.result_text, main_menu_b.text_of_rect)
        else:
            main_menu_b = Button("Главное меню", pygame.font.Font(None, 50), (400, 550), "white", "green")
            main_menu_b.change(pos)
            screen.blit(main_menu_b.result_text, main_menu_b.text_of_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Info.current_level == 4:
                    Info.passed_levels = 4
                    if main_menu_b.check(pos):
                        main_menu()
                        running = False
                else:
                    if next_lvl_b.check(pos):
                        if Info.current_level == Info.passed_levels:
                            Info.passed_levels += 1
                            Info.current_level += 1
                        elif Info.current_level != Info.passed_levels:
                            Info.current_level += 1
                        play(Info.current_level)
                        running = False
                    if main_menu_b.check(pos):
                        if Info.passed_levels >= 4 or Info.current_level != Info.passed_levels:
                            Info.current_level += 1
                        else:
                            Info.current_level += 1
                            Info.passed_levels += 1
                        main_menu()
                        running = False
        pygame.display.flip()


# меню выбора уровня
def level_select():
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
        main_menu_b = Button("Главное меню", pygame.font.Font(None, 50), (200, 550), "white", "green")
        main_menu_b.change(pos)
        screen.blit(main_menu_b.result_text, main_menu_b.text_of_rect)
        if Info.passed_levels == 0:
            color = 'red'
            color_changed = color
        button2 = Button(buttons[1], pygame.font.Font(None, 50), (200 + 200 * 1, 200), color, color_changed)
        button2.change(pos)
        screen.blit(button2.result_text, button2.text_of_rect)
        if Info.passed_levels == 1:
            color = 'red'
            color_changed = color
        button3 = Button(buttons[2], pygame.font.Font(None, 50), (200 + 200 * 2, 200), color, color_changed)
        button3.change(pos)
        screen.blit(button3.result_text, button3.text_of_rect)
        if Info.passed_levels == 2:
            color = 'red'
            color_changed = color
        button4 = Button(buttons[3], pygame.font.Font(None, 50), (300 + 200 * 0, 300), color, color_changed)
        button4.change(pos)
        screen.blit(button4.result_text, button4.text_of_rect)
        if Info.passed_levels == 3:
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
                    Info.current_level = 0
                    play(0)
                    running = False
                if button2.check(pos):
                    if Info.passed_levels > 0:
                        Info.current_level = 1
                        play(1)
                        running = False
                if button3.check(pos):
                    if Info.passed_levels > 1:
                        Info.current_level = 2
                        play(2)
                        running = False
                if button4.check(pos):
                    if Info.passed_levels > 2:
                        Info.current_level = 3
                        play(3)
                        running = False
                if button5.check(pos):
                    if Info.passed_levels > 3:
                        Info.current_level = 4
                        play(4)
                        running = False

                if main_menu_b.check(pos):
                    main_menu()
                    running = False
        pygame.display.flip()


# меню первого открытия игры
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
        text3 = font.render('стрелочек, а также с помощью мышки', True, (255, 255, 255))
        screen.blit(text3, (75, 300))
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


# меню паузы
def pause_game():
    Info.paused = True
    pause_overlay = pygame.Surface((800, 600))
    pause_overlay.set_alpha(128)
    pause_overlay.fill((0, 0, 0))
    font = pygame.font.Font(None, 40)
    text1 = font.render(f'Уровень: {Info.current_level + 1}', True, (255, 255, 255))
    score_text = font.render(f'Счёт: {Info.score}', True, (255, 255, 255))
    font = pygame.font.Font(None, 50)
    message = font.render("Пауза", True, (255, 255, 255))
    message_rect = message.get_rect()
    message_rect.center = (400, 300)
    font = pygame.font.Font(None, 20)
    message1 = font.render("Чтобы продолжить нажмите на любую кнопку", True, (255, 255, 255))
    message_rect1 = message1.get_rect()
    message_rect1.center = (400, 330)
    while Info.paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                Info.paused = False

        screen.blit(pygame.image.load("data\\fon_3.jpg"), (0, 0))
        all_sprites.draw(screen)
        screen.blit(score_text, (650, 0))
        screen.blit(text1, (0, 0))
        screen.blit(pause_overlay, (0, 0))
        screen.blit(message, message_rect)
        screen.blit(message1, message_rect1)
        pygame.display.flip()


# основное меню игры
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
                    play(Info.current_level)
                if exit_b.check(pos):
                    running = False
                if level_choose_b.check(pos):
                    level_select()
        pygame.display.flip()
    pygame.quit()
    sys.exit()


# создаём шарик, платформу и кирпичи
paddle = pygame.sprite.Group()
paddle.add(Paddle(350, 510, 100, 30))
paused = False

# Добавляем спрайты
clock = pygame.time.Clock()
if not os.path.exists('data\\user.txt'):
    data = open('data\\user.txt', 'w')
    data.write('logged\n')
    data.write('0\n')
    data.write('0\n')
    data.write('0\n')
    data.write('0\n')
    data.close()
    Info.score = 0
    Info.high_score = 0
    Info.current_level = 0
    Info.passed_levels = 0
    Info.last_score = 0
    ball = Ball(10, 400, 280)
    first_open()
else:
    data = open('data\\user.txt', 'r')
    lines = data.readlines()
    Info.score = int(lines[1].strip())
    Info.last_score = int(lines[1].strip())
    Info.current_level = int(lines[2].strip())
    Info.passed_levels = int(lines[3].strip())
    Info.high_score = int(lines[4].strip())
    data.close()
    ball = Ball(10, 400, 280)
    main_menu()
