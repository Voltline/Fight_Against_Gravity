import pygame
from pygame import Vector2
from random import randint
import math


class Trace:
    """各种尾迹"""
    __color = [0]*3  # r,g,b

    def __init__(self, settings, loc0: Vector2, loc1: Vector2, born_ms):
        self.loc0 = loc0.copy()
        self.loc1 = loc1.copy()
        self.born_sec = born_ms  # 尾迹出现的时间戳(ms)
        self.life_sec = settings.trace_life_sec  # 尾迹持续的时间(ms)
        self.color = self.get_color()

    def is_alive(self, now_time) -> bool:
        """判断尾迹是否还应该存在"""
        return now_time - self.born_sec < self.life_sec

    def display(self, camera):
        """在screen上绘制"""
        camera.draw_line(self.loc0, self.loc1, self.color)

    # @staticmethod
    def get_color(self) -> (int, int, int):
        """随时间改变颜色"""
        Trace.__color[0] = int((math.cos(((self.born_sec * 50 % 360 - 90) * math.pi) / 360)) ** 2 * 255)
        Trace.__color[1] = int((math.cos(((self.born_sec * 50 % 360 - 90) * math.pi) / 360 - 2 * math.acos(-1) / 3)) ** 2 * 255)
        Trace.__color[2] = int((math.cos(((self.born_sec * 50 % 360 - 90) * math.pi) / 360 + 2 * math.acos(-1) / 3)) ** 2 * 255)
        return Trace.__color[:]
