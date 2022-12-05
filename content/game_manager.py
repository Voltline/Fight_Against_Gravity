import pygame
from pygame import Vector2

from content.ship import Ship
from content.planet import Planet
from content.bullet import Bullet
from content.physics import G


class GameManager:
    """管理游戏状态变量的类"""
    def __init__(self, settings):
        """初始化"""
        self.settings = settings
        self.ships = pygame.sprite.Group()
        self.dead_ships = pygame.sprite.Group()  # 死亡的飞船会加入这个group
        self.planets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.center_v = 0  # 质心的速度
        self.max_dis = 3e3  # 判断子弹消失的距离

    def all_move(self, delta_t):
        """所有objs的移动"""
        for planet in self.planets:
            planet.acc0.update(planet.acc)
            planet.update_loc(delta_t)
        for planet in self.planets:
            planet.update_acc(self.planets)
            planet.update_spd(delta_t)
        for ship in self.ships:
            if ship.is_alive:
                ship.move(delta_t, self.planets)
        for bullet in self.bullets:
            bullet.move(delta_t, self.planets)

    def bullets_disappear(self):
        """让对战斗不会再有影响的子弹消失，从而节省性能"""
        for bullet in self.bullets:  # 实测这样更快
            if bullet.check_del(self.planets, self.ships, self.center_v, self.max_dis):
                self.bullets.remove(bullet)

    def check_bullets_planets_collisions(self):
        """使用圆形碰撞检测"""
        collections = pygame.sprite.groupcollide(
            self.bullets, self.planets, True, False, pygame.sprite.collide_circle)

    def check_ships_bullets_collisions(self):
        """mask检测"""
        collisions = pygame.sprite.groupcollide(
            self.ships, self.bullets, False, True, pygame.sprite.collide_mask)
        for ship, bullets in collisions.items():
            damage = 0
            for bullet in bullets:
                damage += bullet.damage
            ship.hit_bullet(damage, self.ships, self.dead_ships)

    def check_ships_planets_collisions(self):
        """mask检测"""
        collisions = pygame.sprite.groupcollide(
            self.ships, self.planets, False, False, pygame.sprite.collide_mask)
        for ship in collisions.keys():
            ship.die(self.ships, self.dead_ships)

    def check_ships_ships_collisions(self):
        """mask检测"""
        collisions = pygame.sprite.groupcollide(
            self.ships, self.ships, False, False, pygame.sprite.collide_mask)
        for ship1, ship2s in collisions.items():
            for ship2 in ship2s:
                if id(ship1) != id(ship2):
                    ship1.die(self.ships, self.dead_ships)
                    break

    def check_collisions(self):
        self.check_ships_ships_collisions()
        self.check_ships_planets_collisions()
        self.check_ships_bullets_collisions()
        self.check_bullets_planets_collisions()

    def load_map(self, game_map, player_names):
        """加载地图到gm"""
        for group in self.ships, self.dead_ships, self.planets, self.bullets:
            group.empty()
        length = min(len(game_map.ships_info), len(player_names))
        for i in range(length):  # 加载飞船
            loc = game_map.ships_info[i].loc
            spd = game_map.ships_info[i].spd
            angle = game_map.ships_info[i].angle
            player_name = player_names[i]
            ship = Ship(self.settings, loc, spd, angle=angle, player_name=player_name)
            self.ships.add(ship)
        for planet_info in game_map.planets_info:  # 加载星球
            loc = planet_info.loc
            spd = planet_info.spd
            mass = planet_info.mass
            index = planet_info.index
            ratio = planet_info.ratio
            planet = Planet(self.settings, loc, spd, mass, index, ratio)
            self.planets.add(planet)

        self.update_center_v_and_max_dis()   # 计算center_v和max_dis

    def update_center_v_and_max_dis(self):
        """计算center_v和max_dis"""
        sum_m = 0  # 质量总和
        sum_mv = Vector2(0, 0)  # 动量总和
        sum_mr = Vector2(0, 0)  # 位矢总和
        for planet in self.planets:
            sum_m += planet.mass
            sum_mv += planet.mass * planet.spd
            sum_mr += planet.mass * planet.loc
        if sum_m > 0:
            self.center_v = sum_mv / sum_m
            for planet in self.planets:
                other_m = sum_m - planet.mass
                other_mv = sum_mv - planet.spd * planet.mass
                other_v = other_mv / other_m
                v = planet.spd - other_v
                ek = 0.5 * planet.mass * v * v  # 动能
                ep = planet.get_ep(self.planets)  # 势能
                e = ek + ep  # 机械能
                dis = - G * other_m * planet.mass / e
                if dis > self.max_dis:
                    self.max_dis = dis

    def client_update(self, planets_msg=None, all_ships_msg=None, bullets_msg=None, tick=-1):
        """通过msg更新gm"""
        if planets_msg:  # 更新planets
            i = 0
            for planet in self.planets:
                planet.update_by_msg(planets_msg[i], self.planets)
                i += 1
        if all_ships_msg:  # 更新ships和dead_ships
            ships_msg = all_ships_msg[0]
            dead_players_name = all_ships_msg[1]
            for name in dead_players_name:
                for ship in self.ships:
                    if name == ship.player_name:
                        ship.die(self.ships, self.dead_ships)
                        break
            i = 0
            for ship in self.ships:
                ship.update_by_msg(ships_msg[i], self.planets)
                i += 1
        if bullets_msg:  # 更新bullets
            self.bullets.empty()
            for msg in bullets_msg:
                new_bullet = Bullet(self.settings)
                new_bullet.update_by_msg(msg, self.planets)
                new_bullet.loc0.update(new_bullet.loc)
                self.bullets.add(new_bullet)

    @staticmethod
    def group_make_msg(objs: pygame.sprite.Group) -> list:
        """制作一整个group的消息(dead_ships不能用此函数制作消息)"""
        msg = []
        for obj in objs:
            msg.append(obj.make_msg())
        return msg

    def make_planets_msg(self) -> list:
        """制作planets消息"""
        return GameManager.group_make_msg(self.planets)

    def make_ships_msg(self) -> list:
        return GameManager.group_make_msg(self.ships)

    def make_dead_players_name_msg(self) -> list:
        names = []
        for ship in self.dead_ships:
            names.append(ship.player_name)
        return names

    def make_bullets_msg(self) -> list:
        return GameManager.group_make_msg(self.bullets)

    def ships_fire_bullet(self):
        """飞船发射子弹"""
        for ship in self.ships:
            if ship.is_alive and ship.is_fire:
                ship.fire_bullet(self.settings, self.bullets)
