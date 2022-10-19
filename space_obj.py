"""太空中各个对象的基类"""
import pygame
from modules.physics import gvt_acc


class SpaceObj(pygame.sprite.Sprite):
    """太空中各个对象的基类"""
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.loc = pygame.Vector2(0, 0)  # 位置
        self.spd = pygame.Vector2(0, 0)  # 速度
        self.acc = pygame.Vector2(0, 0)  # 加速度
        self.img = pygame.image.load(settings.space_obj_img_path)
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def move(self, delta_t, planets: pygame.sprite.Group):
        """负责该对象的移动,更新loc,spd,acc"""
        self.loc += self.spd * delta_t
        self.spd += self.acc * delta_t
        self.acc.update(0, 0)
        for planet in planets:
            self.acc += gvt_acc(planet.mass, planet.loc, self.loc)

    def display(self):
        """在screen上绘制"""
        self.screen.blit(self.img, self.rect)
