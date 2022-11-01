import pygame


class GameManager:
    """管理游戏状态变量的类"""
    def __init__(self, settings):
        """初始化"""
        self.ships = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
