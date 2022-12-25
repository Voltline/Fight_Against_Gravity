import os

import pygame
import sys
from time import sleep


class HP:
    def __init__(self, x, y, settings):
        self.rect = pygame.Rect(x, y, 60, 10)
        self.r_xy = (0, 0)
        self.path = settings.path

        self.hp = 100
        self.full_hp = self.hp
        self.hp_panel = pygame.image.load(self.path + "assets/Img/hp.png")
        self.hp_column = pygame.transform.smoothscale(pygame.image.load(self.path + "assets/Img/hp_column.png"),
                                                      (self.rect.width, self.rect.height))

    def update_hp(self, new_hp):
        self.hp = new_hp

    def render(self, screen):
        hp = pygame.transform.smoothscale(self.hp_panel, (self.rect.width * self.hp / self.full_hp, self.rect.height))
        screen.blit(hp, (self.rect.left, self.rect.top))
        screen.blit(self.hp_column, (self.rect.left, self.rect.top))


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
        if hpt.hp >= 0:
            hpt.update_hp(hpt.hp-0.1)
        hpt.render(sc)
        pygame.display.flip()
