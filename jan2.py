from random import randrange
import pygame
import math

def speed_reversal(vx, vy, ball, rect):
    if vx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if vy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top
    if delta_x == delta_y:
        vx, vy = -vx, -vy
    elif delta_x > delta_y:
        vy = -vy
    elif delta_y > delta_x:
        vx = -vx
    return vx, vy

size = width, height = 1200, 800
width_of_plat = 330
height_of_plat = 35
speed_of_plat = 15
plat = pygame.Rect(width // 2 - width_of_plat // 2, (height - height_of_plat) % height, width_of_plat, height_of_plat)
radius_of_ball = 20
speed_of_ball = 6
rect_of_ball = int(math.sqrt(2) * radius_of_ball)
ball = pygame.Rect(width // 2, height // 2, rect_of_ball, rect_of_ball)

blocks = [pygame.Rect(120 * i, 70 * j, 120, 70) for i in range(10) for j in range(4)]
color_of_blocks = [(randrange(30, 256), randrange(30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]

vx, vy = 1, -1

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


while True:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill('black')
    pygame.draw.circle(screen, 'white', ball.center, radius_of_ball)
    pygame.draw.rect(screen, 'red', plat)
    for num in range(len(blocks)):
        pygame.draw.rect(screen, color_of_blocks[num], blocks[num])
    # движение шара
    ball.x += vx * speed_of_ball
    ball.y += vy * speed_of_ball
    # столкновение с правой и левой границей
    if ball.center[0] - radius_of_ball < 0 or ball.center[0] + radius_of_ball > width:
        vx = -vx
    # столкновение с верхней границей
    if ball.center[1] - radius_of_ball < 0:
        vy = -vy
    # столкновение с платформой
    if ball.colliderect(plat) and vy > 0:
        vx, vy = speed_reversal(vx, vy, ball, plat)
    # столкновение с блоками
    index = ball.collidelist(blocks)
    if index != -1:
        color = color_of_blocks.pop(index)
        rect = blocks.pop(index)
        vx, vy = speed_reversal(vx, vy, ball, rect)
        # !!!! нужно придумать, что будет после столкновения шарика и блока !!!!
        # rect.inflate_ip(ball.width * 3, ball.height * 3)
        # pygame.draw.rect(screen, color, rect)
    # !!!! нужно придумать, что будет после выигрыша и проигрыша !!!!
    if ball.bottom > height:
        print('GAME OVER!')
        exit()
    elif not len(blocks):
        print('WIN!!!')
        exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT] and plat.right < width:
        plat.right += speed_of_plat
    if key[pygame.K_LEFT] and plat.left > 0:
        plat.left -= speed_of_plat
    pygame.display.flip()
    clock.tick(60)