"""物理计算相关的函数"""
from pygame import Vector2
from math import isclose

G = 6.67408e-11


def gvt_acc(m0: float, loc0: Vector2, loc1: Vector2) -> Vector2:
    """
    计算重力加速度
    m0: 中央星球的质量,单位kg
    loc0: 中央星球的位置
    loc1: 客体的位置
    return: 重力加速度
    """
    ans = loc0 - loc1
    if isclose(0, ans.length()):
        ans.update(0, 0)
    else:
        ans = ans * G * m0 / ans.length()**3

    return ans


def is_close(v1: Vector2, v2: Vector2) -> bool:
    return (v1-v2).length() < 1e-2
