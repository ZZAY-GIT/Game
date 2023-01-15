import pygame
import pygame.mixer
import random

pygame.mixer.init()
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Арканоид")
#СКАЧАЙ ЗВУК
№collision_sound = pygame.mixer.Sound("123.mp3")


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
        self.vx = 2
        self.vy = -2

    def update(self):
        if 0 <= self.rect.x + self.vx <= width - self.radius:
            self.rect = self.rect.move(self.vx, self.vy)
        else:
            self.vx = -self.vx
        if 0 >= self.rect.y - self.radius:
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, paddle):
            self.vy = -self.vy
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

    def update(self):
        pass


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


# создаём шарик, платформу и кирпичи
all_sprites = pygame.sprite.Group()
paddle = pygame.sprite.Group()
ball = Ball(7, 400, 280)
paddle.add(Paddle(350, 510, 100, 10, (255, 255, 255)))
bricks = pygame.sprite.Group()
create_bricks()

# Add the sprites to the group
all_sprites.add(ball, bricks, paddle)
clock = pygame.time.Clock()
moving = False
running = True
while running:
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
    # проверка кубиков



    pygame.display.update()
    screen.fill('black')
    clock.tick(60)

pygame.quit()
