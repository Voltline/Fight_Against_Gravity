import os

import pygame
import sys
from time import sleep


class HP:
    def __init__(self, x, y, path):
        self.left = x
        self.top = y
        self.path = path

        self.width = 90
        self.height = 10
        self.hp_percent = 1
        self.hp_panel = pygame.image.load(self.path + "assets/Img/hp.png")
        self.hp_column = pygame.transform.smoothscale(pygame.image.load(self.path + "assets/Img/hp_column.png"),
                                                      (self.width, self.height))

    def update_hp(self, new_hp_percent):
        self.hp_percent = new_hp_percent

    def render(self, screen):
        hp = pygame.transform.smoothscale(self.hp_panel, (self.width * self.hp_percent, self.height))
        screen.blit(hp, (self.left, self.top))
        screen.blit(self.hp_column, (self.left, self.top))


if __name__ == '__main__':
    fag_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    print(fag_dir)
    os.chdir(fag_dir)
    pygame.init()
    sc = pygame.display.set_mode((1200, 800))
    hpt = HP(100, 100, "")
    while True:
        sc.fill((0, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if hpt.hp_percent >= 0:
            hpt.update_hp(hpt.hp_percent-0.00001)
        hpt.render(sc)
        pygame.display.flip()
