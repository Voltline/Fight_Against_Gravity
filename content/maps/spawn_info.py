"""保存出生点信息的类"""
from pygame import Vector2


class SpawnInfo:
    """出生点信息包括初始位置、初始速度、质量、角度"""
    def __init__(self, loc: Vector2, spd: Vector2, mass=0, angle=0):
        self.loc = loc.copy()
        self.spd = spd.copy()
        if mass:  # 飞船不需要质量参数
            self.mass = mass
        if angle:  # 星球不需要角度参数
            self.angle = angle
