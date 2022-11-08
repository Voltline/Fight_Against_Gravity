import pygame
from pygame import Vector2
from space_obj import SpaceObj


class Planet(SpaceObj):
    """星球"""
    def __init__(self, screen, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0),
                 mass: float = 1):
        super().__init__(screen, settings, 1*loc0, 1*spd0)
        self.mass = mass
        self.radius = self.image.get_rect().width/2

    def __get_image__(self, settings):
        return pygame.image.load(settings.planet_image_path)
