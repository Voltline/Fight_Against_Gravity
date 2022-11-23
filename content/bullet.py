import pygame
from pygame import Vector2
from content.space_obj import SpaceObj


class Bullet(SpaceObj):
    """子弹"""
    # TODO:添加子弹拖尾特效
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0)):
        super().__init__(settings, 1*loc0, 1*spd0)
        self.radius = settings.bullet_radius  # 子弹半径
        self.damage = settings.bullet_damage  # 子弹伤害

    def __get_image__(self, settings):
        return settings.bullet_image
