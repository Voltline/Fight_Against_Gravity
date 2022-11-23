import pygame
from pygame import Vector2
from random import randint


class Trace:
    """各种尾迹"""
    __color = [0]*3  # r,g,b

    def __init__(self, settings, loc0: Vector2, loc1: Vector2, born_ms):
        self.loc0 = loc0.copy()
        self.loc1 = loc1.copy()
        self.color = self.get_color()
        self.born_ms = born_ms  # 尾迹出现的时间戳(ms)
        self.life_ms = settings.trace_life_ms  # 尾迹持续的时间(ms)

    def is_alive(self) -> bool:
        """判断尾迹是否还应该存在"""
        return pygame.time.get_ticks() - self.born_ms < self.life_ms

    def display(self, camera):
        """在screen上绘制"""
        camera.draw_line(self.loc0, self.loc1, self.color)

    @staticmethod
    def get_color() -> (int, int, int):
        """随时间改变颜色"""
        i = randint(0, 4)
        if i < 3:
            Trace.__color[i] = (Trace.__color[i] + 1) % 256
        return Trace.__color[:]
