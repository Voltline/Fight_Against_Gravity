import pygame
from pygame import Vector2
from content.space_objs.space_obj import SpaceObj


class Planet(SpaceObj):
    """
    星球
    由于要并行计算，故星球位置计算不能直接调用move
    """
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0),
                 mass: float = 1, img_index: int = 1, ratio: float = 1.0):
        self.img_index = img_index
        self.ratio = ratio
        super().__init__(settings, 1*loc0, 1*spd0)
        self.mass = mass
        self.radius = self.image.get_rect().width/2
        self.acc0 = Vector2(0, 0)  # 由于星球计算要并行，所以要存储之前的acc

    def __get_image__(self, settings):
        return pygame.transform.rotozoom(pygame.image.load(settings.make_planet_image_path(self.img_index)),
                                         0, self.ratio).convert_alpha()

    def update_spd(self, dt):
        self.spd += (self.acc0 + self.acc) / 2 * dt

    def get_ep(self, planets) -> float:
        """获取引力势能"""
        return self.get_ep_d_m(planets)*self.mass

