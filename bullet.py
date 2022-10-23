import pygame
from pygame import Vector2
from space_obj import SpaceObj


class Bullet(SpaceObj):
    """后期添加子弹拖尾特效"""
    def __init__(self, screen, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0)):
        super().__init__(screen, settings, 1*loc0, 1*spd0)
        self.radius = settings.bullet_radius

    def __get_image__(self, settings):
        return settings.bullet_image
