import sys

import pygame
from pygame import Vector2
from math import sin
from math import cos
from math import degrees
from content.space_objs.space_obj import SpaceObj
from content.space_objs.bullet import Bullet
from content.online.obj_msg import ObjMsg
from content.UI.statusbar_class import StatusBar


class Ship(SpaceObj):
    """玩家操控的飞船"""
    # TODO: 增加尾焰特效；增加玩家抬头信息
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0),
                 angle: float = 0, player_name='?Unknown Player?', is_snapshot=False):
        super().__init__(settings, 1 * loc0, 1 * spd0)
        self.is_snapshot = is_snapshot
        self.image0 = self.image
        self.rect0 = self.image0.get_rect()  # 原始图片的rect
        self.angles = 1440  # 总共有多少角度
        if not self.is_snapshot:
            self.images = [None]*self.angles
            self.rects = [None]*self.angles
            self.masks = [None]*self.angles
            self.make_images_rects_masks()
        self.angle = angle
        self.angle0 = 0
        self.player_name = player_name  # 飞船所属玩家的名字
        self.hp = settings.ship_hp  # 生命值
        self.dead_time = 0  # 死亡时间(sec)

        self.go_acc = settings.ship_go_acc  # 引擎的加速度
        self.turn_spd = settings.ship_turn_spd  # 转向的角速度

        if "--nogui" not in sys.argv and not self.is_snapshot:
            self.status_bar = StatusBar(settings, self.player_name)
            self.explosion_images = self.__get_explosion_images__(settings)
            self.tail_image0 = self.__get_tail_image__(settings)
            self.tail_rect0 = self.tail_image0.get_rect()
            self.tail_image = self.tail_image0.copy()
            self.tail_rect = self.tail_rect0.copy()

        self.update_image()

        # 主动状态
        self.is_go_ahead = False  # 是否在前进
        self.is_go_back = False  # 是否在后退
        self.is_turn_left = False  # 是否在左转
        self.is_turn_right = False  # 是否在右转
        self.is_fire = False  # 是否在开火

        # 被动状态
        self.is_alive = True  # 是否或者

    def __get_image__(self, settings):
        """获取飞船图片"""
        return pygame.image.load(settings.ship_image_path).convert_alpha()

    @staticmethod
    def __get_explosion_images__(settings) -> list:
        """返回按时间顺序的爆炸图片的列表"""
        L = []
        for i in range(0, 10):
            L.append(pygame.image.load(
                settings.make_ship_explosion_image_path(i)).convert_alpha())
        return L

    @staticmethod
    def __get_tail_image__(settings) -> pygame.Surface:
        """返回尾焰图片"""
        return pygame.image.load(settings.ship_tail_image_path).convert_alpha()

    def update_acc(self, planets: pygame.sprite.Group):
        """重载，因为飞船加速度和玩家操作有关"""
        acc0 = self.acc
        self.acc.update(0, 0)
        if self.is_go_ahead:
            self.acc += (self.go_acc * cos(self.angle), self.go_acc * sin(self.angle))
        if self.is_go_back:
            self.acc -= (self.go_acc * cos(self.angle), self.go_acc * sin(self.angle))

        self.acc += self.get_acc_from_planets(planets)
        return acc0

    def update_angle(self, delta_t):
        """根据玩家操作更新飞船朝向的角度"""
        self.angle0 = self.angle
        if self.is_turn_left:
            self.angle -= self.turn_spd * delta_t
        if self.is_turn_right:
            self.angle += self.turn_spd * delta_t

    def move(self, delta_t, planets: pygame.sprite.Group):
        """重载，因为飞船的move还需要update_angle"""
        self.update_angle(delta_t)
        if not self.is_snapshot:
            self.update_image()
        self.update_loc_spd(delta_t, planets)

    def update_image(self):
        """根据飞船目前angle，旋转image0得到目前实际的image"""
        if self.angle != self.angle0:  # 这里用!=判断不是因为忘了float要用isclose
            deg = -degrees(self.angle)
            deg = ((deg % 360) + 360) % 360
            i = int(deg/360*self.angles)
            self.image = self.images[i]
            center = self.rect.center
            self.rect = self.rects[i].copy()
            self.rect.center = center
            self.mask = self.masks[i]

            self.angle0 = self.angle

    def update_tail_image(self):
        """更新尾焰图片"""
        self.tail_image = pygame.transform.rotate(self.tail_image0, -degrees(self.angle))
        self.tail_rect = self.tail_image.get_rect()
        ship_dir = Vector2(cos(self.angle), sin(self.angle))
        self.tail_rect.center = \
            Vector2(self.rect.center) \
            - (self.rect0.width / 2 + self.tail_rect0.width / 2 - 7) * ship_dir

    def make_image_rect_mask_i(self, i: int, n: int):
        """制作第i个角度的image,rect,mask"""
        image = pygame.transform.rotate(self.image0, 360*i/n)
        rect = image.get_rect()
        mask = pygame.mask.from_surface(image)
        return image, rect, mask

    def make_images_rects_masks(self):
        for i in range(self.angles):
            self.images[i], self.rects[i], self.masks[i] =\
                self.make_image_rect_mask_i(i, self.angles)

    def update_explosion_image(self, time):
        """死亡之后的短暂时间里更新爆炸的图片"""
        i = int((time - self.dead_time) / 0.05)
        if "--nogui" not in sys.argv and i < 10 and not self.is_snapshot:
            self.image = self.explosion_images[i]
        else:
            self.image = None

    def display(self, camera):
        if self.image is not None:
            super().display(camera)
        if "--nogui" not in sys.argv and not self.is_snapshot:
            if self.is_alive:  # 还活着就更新并显示status_bar
                self.status_bar.update_hp(self.hp)
                camera.display_status_bar(self.status_bar, self.rect.center, self.rect0.width)
                if self.is_go_ahead:
                    self.update_tail_image()
                    camera.blit(self.tail_image, self.tail_rect)

    def fire_bullet(self, settings, bullets) -> Bullet:
        """
        发射子弹，射速就是物理帧精度
        如果发射了则返回新的子弹，没发射就返回None
        """
        if self.is_fire:
            ship_dir = Vector2(cos(self.angle), sin(self.angle))
            new_bullet_loc = self.loc + 0.6 * self.rect0.width * ship_dir
            new_bullet_spd = self.spd + settings.bullet_spd * ship_dir
            new_bullet = Bullet(settings, new_bullet_loc, new_bullet_spd)
            new_bullet.loc0 = self.loc0 + 0.6 * self.rect0.width * ship_dir
            bullets.add(new_bullet)
            return new_bullet
        else:
            return None

    def die(self, ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group, dead_time: float):
        """死亡时"""
        # TODO:加入死亡特效
        self.is_alive = False
        self.hp = 0
        self.dead_time = dead_time
        if "--nogui" not in sys.argv:
            self.image = self.explosion_images[0]
            self.rect = self.image.get_rect()
        else:
            self.image = None
        self.rect.center = self.loc
        ships.remove(self)
        dead_ships.add(self)

    def check_alive(self, ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group, dead_time: float) -> bool:
        """检查飞船是否还活着，如果死了就执行die函数，返回值为是否活着"""
        if self.hp <= 0:
            self.die(ships, dead_ships, dead_time)
            return False
        return True

    def hit_bullet(self, damage,
                   ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group,
                   time: float):
        """被子弹击中时"""
        # TODO:加入被击中的特效
        self.hp -= damage
        self.check_alive(ships, dead_ships, time)

    def make_ctrl_msg(self) -> list:
        """返回飞船操作状态信息"""
        return list(map(int, [self.is_go_ahead, self.is_go_back,
                              self.is_turn_left, self.is_turn_right,
                              self.is_fire]))

    def load_ctrl_msg(self, msg: list):
        self.is_go_ahead, self.is_go_back, \
            self.is_turn_left, self.is_turn_right, \
            self.is_fire = map(bool, msg)

    def update_by_msg(self, msg: list, planets):
        """通过消息更新自身状态"""
        super().update_by_msg(msg, planets)
        msg = ObjMsg(msg=msg)
        self.angle = msg.angle
        self.hp = msg.hp
        self.load_ctrl_msg(msg.ctrl_msg)

    def copy(self, obj, cpy_ctrl=True):
        """把obj复制到自己，浅拷贝"""
        super().copy(obj)
        self.angle = obj.angle
        self.hp = obj.hp

        if cpy_ctrl:
            self.is_go_ahead = obj.is_go_ahead
            self.is_go_back = obj.is_go_back
            self.is_turn_left = obj.is_turn_left
            self.is_turn_right = obj.is_turn_right
            self.is_fire = obj.is_fire
