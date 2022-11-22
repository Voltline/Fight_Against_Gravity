"""太空中各个对象的基类"""
import pygame
from pygame import Vector2
from modules.physics import gvt_acc


class SpaceObj(pygame.sprite.Sprite):
    """太空中各个对象的基类"""
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0)):
        super().__init__()
        self.loc: Vector2 = loc0  # 位置
        self.spd: Vector2 = spd0  # 速度
        self.acc = Vector2(0, 0)  # 加速度
        self.image = self.__get_image__(settings)
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.mask = pygame.mask.from_surface(self.image)  # 创建记录透明点和不透明点的mask

    def __get_image__(self, settings):
        return pygame.image.load(settings.space_obj_image_path).convert_alpha()

    def get_acc_from_planets(self, planets: pygame.sprite.Group) -> Vector2:
        acc = Vector2(0, 0)
        for planet in planets:
            acc += gvt_acc(planet.mass, planet.loc, self.loc)
        return acc

    def update_acc(self, planets: pygame.sprite.Group) -> Vector2:
        """更新飞船当前的加速度，返回上次的acc"""
        acc0 = self.acc
        self.acc = self.get_acc_from_planets(planets)
        return acc0.copy()

    def update_loc_spd(self, acc0, delta_t):
        """在已经更新了acc后，更新spd和loc"""
        aacc = (self.acc - acc0) / delta_t  # 加加速度
        spd0 = self.spd.copy()
        self.spd += self.acc * delta_t
        self.loc += (self.spd)/1 * delta_t
        # self.loc += (self.acc)/1 * delta_t**2 / 2
        self.loc += aacc * delta_t**3 / 6
        self.rect.center = self.loc

    def move(self, delta_t, planets: pygame.sprite.Group):
        """负责该对象的移动,更新loc,spd,acc"""
        acc0 = self.update_acc(planets)
        self.update_loc_spd(acc0, delta_t)

    def display(self, camera):
        """在screen上绘制"""
        camera.blit(self.image, self.rect)
