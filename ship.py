import pygame
from pygame import Vector2
from math import sin
from math import cos
from math import degrees
from modules.physics import gvt_acc
from space_obj import SpaceObj
from bullet import Bullet


class Ship(SpaceObj):
    """玩家操控的飞船，后期添加尾焰等特效"""
    def __init__(self, screen, settings,
                 loc0: Vector2 = Vector2(0, 0), spd0: Vector2 = Vector2(0, 0),
                 angle: float = 0, player='?Unknown Player?'):
        super().__init__(screen, settings, 1*loc0, 1*spd0)
        self.image0 = self.image
        self.angle = angle
        self.update_image()
        self.player = player  # 飞船所属玩家
        self.hp = settings.ship_hp
        self.go_acc = settings.ship_go_acc
        self.turn_spd = settings.ship_turn_spd

        # 被操作状态
        self.is_go_ahead = False    # 是否在前进
        self.is_go_back = False     # 是否在后退
        self.is_turn_left = False   # 是否在左转
        self.is_turn_right = False  # 是否在右转
        self.is_fire = False        # 是否在开火

    def __get_image__(self, settings):
        return pygame.image.load(settings.ship_image_path).convert_alpha()

    def move(self, delta_t, planets: pygame.sprite.Group = None):
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

        # TODO: 测试阶段后要把if与planets缺省值删掉
        if planets:
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

    def display(self):
        """在screen上绘制"""
        self.screen.blit(self.image, self.rect)

    def fire(self, settings, screen, bullets):
        new_bullet_spd = self.spd + settings.bullet_spd*Vector2(cos(self.angle), sin(self.angle))
        new_bullet = Bullet(screen, settings, self.loc, new_bullet_spd)
        bullets.add(new_bullet)
        self.is_fire = False
