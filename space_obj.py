"""太空中各个对象的基类"""
import pygame
from pygame import Vector2
from modules.physics import gvt_acc


class SpaceObj(pygame.sprite.Sprite):
    """太空中各个对象的基类"""
    def __init__(self, screen, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0)):
        super().__init__()
        self.screen = screen
        self.loc: Vector2 = loc0  # 位置
        self.spd: Vector2 = spd0  # 速度
        self.acc = Vector2(0, 0)  # 加速度
        self.image = self.__get_image__(settings)
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.mask = pygame.mask.from_surface(self.image)  # 创建记录透明点和不透明点的mask

    def __get_image__(self, settings):
        return pygame.image.load(settings.space_obj_image_path)

    def move(self, delta_t, planets: pygame.sprite.Group):
        """负责该对象的移动,更新loc,spd,acc"""
        self.acc.update(0, 0)
        for planet in planets:
            self.acc += gvt_acc(planet.mass, planet.loc, self.loc)
        self.loc += self.spd * delta_t
        self.rect.center = self.loc
        self.spd += self.acc * delta_t

    def display(self):
        """在screen上绘制"""
        self.screen.blit(self.image, self.rect)
