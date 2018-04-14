# -*- coding: utf-8 -*-
"""
壁球游戏自修改class版本。
"""
import pygame


class BallGame:
    def __init__(self):
        pygame.init()
        self.size = (1000, 600)
        self.speed = [1, 1]
        self.BLACK = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('BallGame')
        self.fps = 300
        self.fclock = pygame.time.Clock()
        self.hold = False

        imgpath = 'resource/PYG02-ball.gif'
        self.load_ballimg(imgpath)
        self.run()

    def load_ballimg(self, imgpath):
        self.ball = pygame.image.load(imgpath)
        self.ballrect = self.ball.get_rect()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.kb_speed_control(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.hold = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.hold == False
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] == 1:
                        ballrect = self.ballrect.move(event.pos[0] - self.ballrect.left, event.pos[1] - self.ballrect.top)
                        if ballrect.bottomright <= self.size:
                            self.ballrect = ballrect
                        elif ballrect.right > self.size[0] and ballrect.bottom <= self.size[1]:
                            self.ballrect = self.ballrect.move(0, event.pos[1] - self.ballrect.top)
                        elif ballrect.bottom > self.size[1] and ballrect.right <= self.size[0]:
                            self.ballrect = self.ballrect.move(event.pos[0] - self.ballrect.left, 0)
            self.refresh_screen()

    def kb_speed_control(self, event):
        sign_td = 1 if self.speed[0] >= 0 else -1
        sign_lr = 1 if self.speed[1] >= 0 else -1
        if event.key == pygame.K_LEFT:
            self.speed[0] = sign_td * (abs(self.speed[0]) - 1) if self.speed[0] != 0 else 0
        elif event.key == pygame.K_RIGHT:
            self.speed[0] = sign_td * (abs(self.speed[0]) + 1)
        elif event.key == pygame.K_UP:
            self.speed[1] = sign_lr * (abs(self.speed[1]) + 1)
        elif event.key == pygame.K_DOWN:
            self.speed[1] = sign_lr * (abs(self.speed[1]) - 1) if self.speed[1] != 0 else 0

    def refresh_screen(self):
        if self.ballrect.left < 0 or self.ballrect.right > self.size[0]:
            self.speed[0] = - self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > self.size[1]:
            self.speed[1] = - self.speed[1]
        if not self.hold:
            self.ballrect = self.ballrect.move(*self.speed)
        
        self.screen.fill(self.BLACK)
        self.screen.blit(self.ball, self.ballrect)
        pygame.display.update()
        self.fclock.tick(self.fps)


if __name__ == '__main__':
    BallGame()
