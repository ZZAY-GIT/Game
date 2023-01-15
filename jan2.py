import sys
import pygame


# класс мячика
class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 4
        self.vy = -4

    def update(self):
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
    def __init__(self, x, y, width, height, color):
        super().__init__(all_sprites)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def update(self, direction):
        if direction == 'right':
            if self.rect.x + 5 <= width - self.width:
                self.rect = self.rect.move(5, 0)
        else:
            if self.rect.x - 5 >= 0:
                self.rect = self.rect.move(-5, 0)


# класс кирпича
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__(all_sprites)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.color = color


# создание кирпичей
def create_bricks():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    x_pos = 50
    y_pos = 50
    for i in range(3):
        for j in range((width - 100) // 50):
            bricks.add(Brick(x_pos, y_pos, 50, 25, colors[i]))
            x_pos += 50
        x_pos = 50
        y_pos += 25


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


pygame.init()
pygame.mixer.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
collision_sound = pygame.mixer.Sound("123.mp3")
# создаём шарик, платформу и кирпичи
all_sprites = pygame.sprite.Group()
paddle = pygame.sprite.Group()
ball = Ball(7, 400, 280)
paddle.add(Paddle(350, 510, 100, 10, (255, 255, 255)))
bricks = pygame.sprite.Group()
create_bricks()
# Добавляем спрайты
all_sprites.add(ball, bricks, paddle)
clock = pygame.time.Clock()


def play():
    pygame.display.set_caption("Арканоид")
    running = True
    moving = False
    while running:
        screen.blit(pygame.image.load("fon_3.jpg"), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

        all_sprites.draw(screen)
        ball.update()
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


def main_menu():
    pygame.display.set_caption("Меню")
    running = True
    while running:
        screen.blit(pygame.image.load("fon_2.jpg"), (0, 0))
        play_b = Button("ИГРАТЬ", pygame.font.Font(None, 75), (200, 300), "white", "green")
        exit_b = Button("ВЫЙТИ", pygame.font.Font(None, 75), (600, 300), "white", "red")
        text_of_menu = pygame.font.Font(None, 100).render("МЕНЮ", True, "white")
        rect_of_menu = text_of_menu.get_rect(center=(400, 100))
        screen.blit(text_of_menu, rect_of_menu)
        pos = pygame.mouse.get_pos()
        play_b.change(pos)
        screen.blit(play_b.result_text, play_b.text_of_rect)
        exit_b.change(pos)
        screen.blit(exit_b.result_text, exit_b.text_of_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_b.check(pos):
                    play()
                if exit_b.check(pos):
                    running = False
        pygame.display.flip()
    pygame.quit()
    sys.exit()

main_menu()
