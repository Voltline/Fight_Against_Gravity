import pygame
from content.ship import Ship
from content.planet import Planet
from content.bullet import Bullet


class GameManager:
    """管理游戏状态变量的类"""
    def __init__(self, settings):
        """初始化"""
        self.settings = settings
        self.ships = pygame.sprite.Group()
        self.dead_ships = pygame.sprite.Group()  # 死亡的飞船会加入这个group
        self.planets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

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
        for planet_info in game_map.planets_info:
            loc = planet_info.loc
            spd = planet_info.spd
            mass = planet_info.mass
            planet = Planet(self.settings, loc, spd, mass=mass)
            self.planets.add(planet)

    def client_update(self, planets_msg=None, all_ships_msg=None, bullets_msg=None):
        """通过msg更新gm"""
        if planets_msg:  # 更新planets
            i = 0
            for planet in self.planets:
                planet.update_by_msg(planets_msg[i])
                i += 1
        if all_ships_msg:  # 更新ships和dead_ships
            ships_msg = all_ships_msg[0]
            dead_players_name = all_ships_msg[1]
            for name in dead_players_name:
                for ship in self.ships:
                    if name == ship.player_name:
                        ship.die()
                        break
            i = 0
            for ship in self.ships:
                ship.update_by_msg(ships_msg[i])
                i += 1
        if bullets_msg:  # 更新bullets
            self.bullets.empty()
            for msg in bullets_msg:
                self.bullets.add(Bullet(self.settings).update_by_msg(msg))

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
