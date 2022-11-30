import pygame
from pygame import Vector2
from content.space_obj import SpaceObj


class Bullet(SpaceObj):
    """子弹"""
    # TODO:添加子弹拖尾特效

    COLOR = (0, 0, 0)

    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0)):
        super().__init__(settings, 1*loc0, 1*spd0)
        self.radius = settings.bullet_radius  # 子弹半径
        self.damage = settings.bullet_damage  # 子弹伤害
        self.can_escape = -1  # 能否逃逸; -1:未计算

    @staticmethod
    def init(settings):
        Bullet.COLOR = settings.bullet_color

    def __get_image__(self, settings):
        return settings.bullet_image

    def display(self, camera):
        super().display(camera)
        camera.draw_dot(Vector2(self.rect.center), Bullet.COLOR)

    def update_can_escape(self, planets, center_v: Vector2):
        """只有在can_escape<0时调用一次"""
        ekdm = self.get_ek_d_m(center_v)
        epdm = self.get_ep_d_m(planets)
        if ekdm+epdm >= -0:
            self.can_escape = 1
        else:
            self.can_escape = 0

    def check_del(self, planets, center_v: Vector2, max_dis: float) -> bool:
        """检查是否需要删除"""
        if self.can_escape < 0:
            self.update_can_escape(planets, center_v)
        min_dis = 0  # 所有距离中最小的
        for planet in planets:
            dis = (self.loc-planet.loc).length()  # 这个距离
            if dis < min_dis or min_dis == 0:
                min_dis = dis
        if self.can_escape > 0 and min_dis > max_dis\
                or min_dis > 3*max_dis:
            return True
        return False
