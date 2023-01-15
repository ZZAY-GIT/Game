import pygame

# Initialize pygame and set up the game window
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arkanoid")


# класс мячика
class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.dx = speed
        self.dy = -speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x + self.radius > width or self.x - self.radius < 0:
            self.dx = -self.dx
        if self.y - self.radius < 0:
            self.dy = -self.dy
        if self.y + self.radius >= height:
            print('Проиграли!')
            pygame.quit()

    # проверка столкновения
    def collides_with(self, obj):
        if isinstance(obj, Paddle):
            if (self.x > obj.x and self.x < obj.x + obj.width) and (self.y + self.radius > obj.y):
                return True
        elif isinstance(obj, Brick):
            if (self.x + self.radius > obj.x) and (self.x - self.radius < obj.x + obj.width) and (
                    self.y + self.radius > obj.y) and (self.y - self.radius < obj.y + obj.height):
                return True
        else:
            return False

    def bounce(self):
        self.dy = -self.dy


# класс платформы
class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def move_left(self):
        if self.x >= 0:
            self.x -= self.speed

    def move_right(self):
        if self.x <= width - self.width:
            self.x += self.speed


# класс кирпича
class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.destroyed = False

    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)

    def hit(self):
        self.destroyed = True

    def is_destroyed(self):
        return self.destroyed


# создание кирпичей
def create_bricks():
    bricks = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    x_pos = 50
    y_pos = 50
    for i in range(3):
        for j in range((width-100)//50):
            bricks.append(Brick(x_pos, y_pos, 50, 25, colors[i]))
            x_pos += 50
        x_pos = 50
        y_pos += 25
    return bricks


# создаём шарик, платформу и кирпичи
ball = Ball(400, 280, 5, 2)
paddle = Paddle(350, 500, 100, 10, 5)
bricks = create_bricks()

clock = pygame.time.Clock()
moving = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
        if event.type == pygame.MOUSEBUTTONUP:
            moving = False
    # передвижение с помощью клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left()
    if keys[pygame.K_RIGHT]:
        paddle.move_right()
    # передвижение с помощью мышки
    if moving:
        cursor_x, cursor_y = pygame.mouse.get_pos()
        paddle.x = cursor_x - paddle.width // 2
        if paddle.x < 0:
            paddle.x = 0
        elif paddle.x + paddle.width > width:
            paddle.x = width - paddle.width
    # шарик двигается и проверяет столкновение
    ball.move()
    if ball.collides_with(paddle):
        ball.bounce()
    for brick in bricks:
        if ball.collides_with(brick):
            ball.bounce()
            brick.hit()
            if brick.is_destroyed():
                bricks.remove(brick)
    screen.fill((0, 0, 0))
    ball.draw(screen)
    paddle.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
