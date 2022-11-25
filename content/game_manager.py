import pygame


class GameManager:
    """管理游戏状态变量的类"""
    def __init__(self):
        """初始化"""
        self.ships = pygame.sprite.Group()
        self.dead_ships = pygame.sprite.Group()  # 死亡的飞船会加入这个group
        self.planets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
