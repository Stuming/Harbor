# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 20:49:31 2018

@author: Stuming
"""

import numpy as np
import matplotlib.pyplot as plt
import pygame
import time

MAX_COLOR = 255


def plot_mandelbrot(iterations=10):
    """
    Plot mandelbrot fractal image by matplotlib.
    
    Parameters
    ----------
        iterations: times of iterations in algorithms.
    """
    x_extent = (-2.5, 1)
    y_extent = (-1, 1)
    size = 200
    
    x, y = np.meshgrid(np.linspace(*x_extent, size), 
                       np.linspace(*y_extent, size))
    c = x + 1j * y
    z = c.copy()
    fractal = np.zeros(z.shape, dtype=np.uint8) + MAX_COLOR
    
    for n in range(iterations):
        mask = np.abs(z) <= 4
        z[mask] = z[mask] ** 2 + c[mask]
        fractal[(fractal==MAX_COLOR)&(~mask)] = MAX_COLOR * n / iterations
        
    plt.imshow(fractal)
    plt.title('Mandelbrot(iter={})'.format(n+1))
    plt.axis('off')
    plt.show()


class FractalPlot():
    """
    Plot fractal image by pygame, and try to display its dynamic changes.
    
    Parameters
    ----------
        iterations: times of iterations in algorithms.
        speed: figure display speed, duration = 1/speed (s)
    """
    def __init__(self, iterations=10, speed=1):
        pygame.init()
        self.size = 600
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption('Mandelbrot')
        
        self.iterations = iterations
        self.sleeptime = 1 / speed

        self.mandelbrot()
        
        time.sleep(self.sleeptime)
        pygame.quit()
        
    def mandelbrot(self):
        x_extent = (-2.5, 1)
        y_extent = (-1, 1)
        x, y = np.meshgrid(np.linspace(*x_extent, self.size), 
                           np.linspace(*y_extent, self.size))
        c = x + 1j * y
        z = c.copy()
        fractal = np.zeros(z.shape, dtype=np.uint8) + MAX_COLOR

        for n in range(self.iterations):
            mask = np.abs(z) <= 4
            z[mask] = z[mask] ** 2 + c[mask]
            fractal[(fractal==MAX_COLOR)&(~mask)] = MAX_COLOR \
                * n / self.iterations
            
            # TODO transform gray(or any single color) to RGB
            screenarray = np.reshape([fractal]*3, (*fractal.shape, 3))
            # screenarray = np.zeros((*self.size, 3))
            # screenarray[:, :, 0] = fractal

            pygame.display.set_caption('Mandelbrot(iter={})'.format(n+1))
            # TODO this method shows 9 fractal images, better shows 1.
            pygame.surfarray.blit_array(self.screen, screenarray)
            pygame.display.flip()
            time.sleep(self.sleeptime)
            print(screenarray.shape)


if __name__ == '__main__':
    plot_mandelbrot(100)
    