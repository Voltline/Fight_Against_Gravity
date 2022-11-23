"""太空中各个对象的基类"""
import pygame
from pygame import Vector2
from content.physics import gvt_acc


class SpaceObj(pygame.sprite.Sprite):
    """太空中各个对象的基类"""
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0)):
        super().__init__()
        self.loc: Vector2 = loc0.copy()  # 位置
        self.loc0 = self.loc.copy()  # 上一次的位置, 用于线性插值
        self.loc00 = self.loc.copy()  # 上一次渲染的位置，用于记录尾迹
        self.spd: Vector2 = spd0.copy()  # 速度
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

    def update_loc_spd(self, dt, planets: pygame.sprite.Group):
        """
        在已经更新了acc后，更新spd和loc

        误差不太大的组合：
        x'用spd,x"不用,x"'用
        x'用(spd+spd0)/2,x"用(acc+acc0)/2,x"'用

        """
        spd0 = self.spd.copy()
        acc0 = self.acc.copy()
        spd = self.spd
        # 韦尔莱算法
        self.update_loc(dt)
        self.update_acc(planets)
        self.spd += (acc0 + self.acc)/2 * dt

        # 自己瞎写的算法
        # self.spd += self.acc * delta_t + aacc * delta_t**2 / 2
        # self.loc += (0.5*spd0+0.5*spd) * delta_t
        # self.loc += (0.5*acc0+0.5*acc) * delta_t**2 / 2
        # self.loc += aacc * delta_t**3 / 6

    def update_loc(self, dt):
        """下一时刻的位置需要这一时刻的速度和加速度"""
        self.loc0.update(self.loc)
        self.loc += self.spd * dt + self.acc * dt * dt / 2
        self.rect.center = self.loc

    def move(self, delta_t, planets: pygame.sprite.Group):
        """
        负责该对象的移动,更新loc,spd,acc
        之所以开move函数是为了方便ship重载
        """
        self.update_loc_spd(delta_t, planets)

    def display(self, camera):
        """在screen上绘制"""

        camera.blit(self.image, self.rect)
