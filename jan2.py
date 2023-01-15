import pygame

# Initialize pygame and set up the game window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Arkanoid")


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

        if self.x + self.radius > 800 or self.x - self.radius < 0:
            self.dx = -self.dx
        if self.y - self.radius < 0:
            self.dy = -self.dy

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
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed


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

    def hit(self):
        self.destroyed = True

    def is_destroyed(self):
        return self.destroyed


def create_bricks():
    bricks = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    x_pos = 0
    y_pos = 50
    for i in range(3):
        for j in range(10):
            bricks.append(Brick(x_pos, y_pos, 75, 25, colors[i]))
            x_pos += 75
        x_pos = 0
        y_pos += 25
    return bricks


# Create the ball, paddle, and bricks
ball = Ball(400, 280, 5, 2)
paddle = Paddle(350, 500, 100, 10, 5)
bricks = create_bricks()

clock = pygame.time.Clock()
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddle based on user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left()
    if keys[pygame.K_RIGHT]:
        paddle.move_right()

    # Move the ball and check for collisions
    ball.move()
    if ball.collides_with(paddle):
        ball.bounce()
    for brick in bricks:
        if ball.collides_with(brick):
            ball.bounce()
            brick.hit()
            if brick.is_destroyed():
                bricks.remove(brick)

    # Draw the game elements to the screen
    screen.fill((0, 0, 0))
    ball.draw(screen)
    paddle.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    pygame.display.update()
    clock.tick(144)
# Clean up and exit
pygame.quit()
