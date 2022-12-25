import sys
import time

import pygame
from settings.all_settings import Settings
import os


class ScrollBar:
    def __init__(self, rect: list, settings):
        self.left, self.top, self.height = rect
        print("bar height", self.height)
        self.width = 18
        self.is_dragging = False
        self.bar_thumb = [pygame.image.load(settings.thumb),
                          pygame.image.load(settings.thumb_pressed)]
        self.thumb_width, self.thumb_height = 10, 60
        self.thumb_left = self.left + (self.width-self.thumb_width)/2
        self.thumb_top = self.top
        self.thumb_status = 0  # 对应显示状态，动态效果
        for i in range(len(self.bar_thumb)):
            self.bar_thumb[i] = pygame.transform.smoothscale(self.bar_thumb[i], (self.thumb_width, self.thumb_height))
        self.bar = pygame.image.load(settings.bar)
        self.bar = pygame.transform.smoothscale(self.bar, (self.width, self.height))
        # self.ratio = (self.thumb_top-self.top)/(self.height - self.thumb_height)

    @property
    def ratio(self) -> float:
        """返回[0,1]之间的浮点数"""
        return (self.thumb_top-self.top)/(self.height - self.thumb_height)

    def render(self, screen, top):
        screen.blit(self.bar, (self.left, top + self.top))
        screen.blit(self.bar_thumb[self.thumb_status], (self.thumb_left, top + self.thumb_top))

    def deal_event(self, e, pos_offset=(0, 0)):
        rect = pygame.Rect((self.thumb_left, self.thumb_top, self.thumb_width, self.thumb_height))
        if e.type == pygame.MOUSEWHEEL:
            if e.y > 0:
                self.thumb_top -= 18
            else:
                self.thumb_top += 18
        if e.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(e.pos[0]-pos_offset[0], e.pos[1]-pos_offset[1]):
                self.is_dragging = True
        elif e.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif e.type == pygame.MOUSEMOTION:
            if rect.collidepoint(e.pos[0]-pos_offset[0], e.pos[1]-pos_offset[1]):
                self.thumb_status = 1
            elif self.is_dragging:
                self.thumb_status = 1
            else:
                self.thumb_status = 0
            if self.is_dragging:
                self.thumb_top = e.pos[1]-pos_offset[1]
        self.thumb_top = max(self.top, min(self.thumb_top, self.top + self.height - self.thumb_height))


if __name__ == "__main__":
    pygame.init()
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'
    settings_ = Settings(path)
    sc = pygame.display.set_mode((1200, 800))
    sc.fill((10, 10, 10))
    sb = ScrollBar([1150, 0, 800], settings_)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            sb.deal_event(event)
        sb.render(sc)
        pygame.display.flip()
