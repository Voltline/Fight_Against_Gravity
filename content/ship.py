import pygame
from pygame import Vector2
from math import sin
from math import cos
from math import degrees
from content.space_obj import SpaceObj
from content.bullet import Bullet


class Ship(SpaceObj):
    """玩家操控的飞船"""
    # TODO:添加尾焰等特效
    def __init__(self, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0),
                 angle: float = 0, player_name='?Unknown Player?'):
        super().__init__(settings, 1*loc0, 1*spd0)
        self.image0 = self.image
        self.angle = angle
        self.update_image()
        self.player_name = player_name  # 飞船所属玩家的名字
        self.hp = settings.ship_hp  # 生命值
        self.go_acc = settings.ship_go_acc  # 引擎的加速度
        self.turn_spd = settings.ship_turn_spd  # 转向的角速度
        self.fired_time = 0  # 上次发射子弹的时间戳(s)
        self.fire_rate = settings.ship_fire_rate  # 飞船射速(发/秒)

        # 主动状态
        self.is_go_ahead = False    # 是否在前进
        self.is_go_back = False     # 是否在后退
        self.is_turn_left = False   # 是否在左转
        self.is_turn_right = False  # 是否在右转
        self.is_fire = False        # 是否在开火

        # 被动状态
        self.is_alive = True  # 是否或者

    def __get_image__(self, settings):
        """获取飞船图片"""
        return pygame.image.load(settings.ship_image_path).convert_alpha()

    def update_acc(self, planets: pygame.sprite.Group):
        """重载，因为飞船加速度和玩家操作有关"""
        acc0 = self.acc
        self.acc.update(0, 0)
        if self.is_go_ahead:
            self.acc += (self.go_acc*cos(self.angle), self.go_acc*sin(self.angle))
        if self.is_go_back:
            self.acc -= (self.go_acc * cos(self.angle), self.go_acc * sin(self.angle))

        self.acc += self.get_acc_from_planets(planets)
        return acc0

    def update_angle(self, delta_t):
        """根据玩家操作更新飞船朝向的角度"""
        if self.is_turn_left:
            self.angle -= self.turn_spd * delta_t
        if self.is_turn_right:
            self.angle += self.turn_spd * delta_t
        if self.is_turn_left ^ self.is_turn_right:
            self.update_image()

    def move(self, delta_t, planets: pygame.sprite.Group):
        """重载，因为飞船的move还需要update_angle"""
        self.update_angle(delta_t)
        self.update_loc_spd(delta_t, planets)

    def update_image(self):
        """根据飞船目前angle，旋转image0得到目前实际的image"""
        self.image = pygame.transform.rotate(self.image0, -degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.mask = pygame.mask.from_surface(self.image)  # 更新mask

    def fire_bullet(self, settings, bullets):
        """发射子弹"""
        if self.is_fire:
            now_time = pygame.time.get_ticks() / 1000  # 当前时间戳(秒)
            if now_time - self.fired_time >= 1 / self.fire_rate:  # 限制射速
                self.fired_time = now_time
                ship_dir = Vector2(cos(self.angle), sin(self.angle))
                new_bullet_loc = self.loc + 0.6*self.image0.get_width()*ship_dir
                new_bullet_spd = self.spd + settings.bullet_spd * ship_dir
                new_bullet = Bullet(settings, new_bullet_loc, new_bullet_spd)
                bullets.add(new_bullet)

    def die(self, ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group):
        """死亡时"""
        # TODO:加入死亡特效
        self.is_alive = False
        self.hp = 0
        ships.remove(self)
        dead_ships.add(self)

    def check_alive(self, ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group) -> bool:
        """检查飞船是否还活着，如果死了就执行die函数，返回值为是否活着"""
        if self.hp <= 0:
            self.die(ships, dead_ships)
            return False
        return True

    def hit_bullet(self, damage,
                   ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group):
        """被子弹击中时"""
        # TODO:加入被击中的特效
        self.hp -= damage
        self.check_alive(ships, dead_ships)

    def make_msg(self) -> dict:
        """重载，飞船还需要传输player_name和angle"""
        msg = super().make_msg()
        msg['player_name'] = self.player_name
        msg['angle'] = self.angle
        return msg
