"""物理计算相关的函数"""
import pygame

G = 6.67408e-11


def gvt_acc(m0: float, loc0: pygame.Vector2, loc1: pygame.Vector2) -> pygame.Vector2:
    """
    计算重力加速度
    m0: 中央星球的质量,单位kg
    loc0: 中央星球的位置
    loc1: 客体的位置
    return: 重力加速度
    """
    ans = loc0 - loc1
    ans = ans * G * m0 / ans.length()**3
    return ans
