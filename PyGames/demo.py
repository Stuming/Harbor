import sys
import pygame


pygame.init()
size = (1000, 600)
speed = [1, 1]
BLACK = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyGames')
ball = pygame.image.load('resource/PYG02-ball.gif')
ballrect = ball.get_rect()
fps = 300
fclock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    ballrect = ballrect.move(speed[0], speed[1])
    if ballrect.left < 0 or ballrect.right > size[0]:
        speed[0] = - speed[0]
    if ballrect.top < 0 or ballrect.bottom > size[1]:
        speed[1] = - speed[1]

    screen.fill(BLACK)
    screen.blit(ball, ballrect)
    pygame.display.update()
    fclock.tick(fps)