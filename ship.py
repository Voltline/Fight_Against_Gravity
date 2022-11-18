import pygame
from pygame import Vector2
from math import sin
from math import cos
from math import degrees
from modules.physics import gvt_acc
from space_obj import SpaceObj
from bullet import Bullet


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
        self.hp = settings.ship_hp
        self.go_acc = settings.ship_go_acc
        self.turn_spd = settings.ship_turn_spd

        # 主动状态
        self.is_go_ahead = False    # 是否在前进
        self.is_go_back = False     # 是否在后退
        self.is_turn_left = False   # 是否在左转
        self.is_turn_right = False  # 是否在右转
        self.is_fire = False        # 是否在开火

        # 被动状态
        self.is_alive = True  # 是否或者

    def __get_image__(self, settings):
        return pygame.image.load(settings.ship_image_path).convert_alpha()

    def move(self, delta_t, planets: pygame.sprite.Group):
        self.acc.update(0, 0)
        if self.is_go_ahead:
            self.acc += (self.go_acc*cos(self.angle), self.go_acc*sin(self.angle))
        if self.is_go_back:
            self.acc -= (self.go_acc * cos(self.angle), self.go_acc * sin(self.angle))

        if self.is_turn_left:
            self.angle -= self.turn_spd * delta_t
        if self.is_turn_right:
            self.angle += self.turn_spd * delta_t
        if self.is_turn_left ^ self.is_turn_right:
            self.update_image()

        for planet in planets:
            self.acc += gvt_acc(planet.mass, planet.loc, self.loc)

        self.loc += self.spd * delta_t
        self.rect.center = self.loc
        self.spd += self.acc * delta_t

    def update_image(self):
        self.image = pygame.transform.rotate(self.image0, -degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.mask = pygame.mask.from_surface(self.image)  # 更新mask

    def fire_bullet(self, settings, bullets):
        ship_dir = Vector2(cos(self.angle), sin(self.angle))
        new_bullet_loc = self.loc + 0.6*self.image0.get_width()*ship_dir
        new_bullet_spd = self.spd + settings.bullet_spd * ship_dir
        new_bullet = Bullet(settings, new_bullet_loc, new_bullet_spd)
        bullets.add(new_bullet)
        self.is_fire = False

    def die(self, ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group):
        """死亡时"""
        # TODO:加入死亡特效
        self.is_alive = False
        self.hp = 0
        ships.remove(self)
        dead_ships.add(self)

    def check_alive(self, ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group):
        if self.hp <= 0:
            self.die(ships, dead_ships)

    def hit_bullet(self, damage,
                   ships: pygame.sprite.Group, dead_ships: pygame.sprite.Group):
        """被子弹击中时"""
        # TODO:加入被击中的特效
        self.hp -= damage
        self.check_alive(ships, dead_ships)
