import os

import pygame
import sys
from time import sleep

class HP:
    def __init__(self, x, y):
        self.left = x
        self.top = y
        self.width = 60
        self.height = 6
        self.hp_percent = 1
        self.hp_panel = pygame.image.load("assets/Img/hp.png")

    def render(self, screen):
        hp = pygame.transform.smoothscale(self.hp_panel, (self.width * self.hp_percent, self.height))
        screen.blit(hp, (self.left, self.top))


if __name__ == '__main__':
    fag_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    print(fag_dir)
    os.chdir(fag_dir)
    pygame.init()
    sc = pygame.display.set_mode((1200, 800))
    hpt = HP(100, 100)
    while True:
        sc.fill((0, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if hpt.hp_percent >= 0:
            hpt.hp_percent -= 0.000001
        hpt.render(sc)
        pygame.display.flip()
