import pygame
from pygame import Vector2
from content.space_obj import SpaceObj


class Planet(SpaceObj):
    """
    星球
    由于要并行计算，故星球位置计算不能直接调用move
    """
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0),
                 mass: float = 1):
        super().__init__(settings, 1*loc0, 1*spd0)
        self.mass = mass
        self.radius = self.image.get_rect().width/2
        self.acc0 = Vector2(0, 0)  # 由于星球计算要并行，所以要存储之前的acc

    def __get_image__(self, settings):
        return pygame.image.load(settings.planet_image_path).convert_alpha()

    def update_spd(self, dt):
        self.spd += (self.acc0 + self.acc) / 2 * dt

    # def update_loc_spd(self, dt, planets: pygame.sprite.Group):
    #     """
    #     在已经更新了acc后，更新spd和loc
    #
    #     误差不太大的组合：
    #     x'用spd,x"不用,x"'用
    #     x'用(spd+spd0)/2,x"用(acc+acc0)/2,x"'用
    #     """
    #     aacc = (self.acc - acc0) / dt  # 加加速度
    #     spd0 = self.spd.copy()
    #     acc = self.acc
    #     spd = self.spd
    #     self.spd += self.acc * dt
    #     self.loc += (0.6*spd0+0.4*spd) * dt
    #     self.loc += (0.5*acc0+0.5*acc) * dt ** 2 / 2
    #     self.loc += aacc * dt ** 3 / 6
    #     self.rect.center = self.loc
