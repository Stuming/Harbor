# -*- coding: utf-8 -*-
"""
壁球游戏，源自MOOC课程《python游戏开发入门》，http://www.icourse163.org/course/BIT-1001873001
"""
import sys
import pygame


pygame.init()
size = (1000, 600)
speed = [1, 1]
BLACK = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.display.set_caption('BallGame')
ball = pygame.image.load('resource/PYG02-ball.gif')
ballrect = ball.get_rect()
fps = 300
fclock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            sign_td = 1 if speed[0] >= 0 else -1
            sign_lr = 1 if speed[1] >= 0 else -1
            # K_RIGHT/K_UP stands for speeding up, and K_LEFT/K_DOWN for slowing down.
            if event.key == pygame.K_LEFT:
                speed[0] = sign_td * (abs(speed[0]) - 1) if speed[0] != 0 else 0
            elif event.key == pygame.K_RIGHT:
                speed[0] = sign_td * (abs(speed[0]) + 1)
            elif event.key == pygame.K_UP:
                speed[1] = sign_lr * (abs(speed[1]) + 1)
            elif event.key == pygame.K_DOWN:
                speed[1] = sign_lr * (abs(speed[1]) - 1) if speed[1] != 0 else 0

    ballrect = ballrect.move(speed[0], speed[1])
    if ballrect.left < 0 or ballrect.right > size[0]:
        speed[0] = - speed[0]
    if ballrect.top < 0 or ballrect.bottom > size[1]:
        speed[1] = - speed[1]

    screen.fill(BLACK)
    screen.blit(ball, ballrect)
    pygame.display.update()
    fclock.tick(fps)
