import pygame
from content.ship import Ship
from content.planet import Planet

class GameManager:
    """管理游戏状态变量的类"""
    def __init__(self):
        """初始化"""
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

    def load_map(self, settings, game_map, player_names):
        """加载地图到gm"""
        for group in self.ships, self.dead_ships, self.planets, self.bullets:
            group.clear()
        length = min(len(game_map.ships_info), len(player_names))
        for i in range(length):  # 加载飞船
            loc = game_map.ships_info[i].loc
            spd = game_map.ships_info[i].spd
            angle = game_map.ships_info[i].angle
            player_name = player_names[i]
            ship = Ship(settings, loc, spd, angle=angle, player_name=player_name)
            self.ships.add(ship)
        for planet_info in game_map.planets_info:
            loc = planet_info.loc
            spd = planet_info.spd
            mass = planet_info.mass
            planet = Planet(settings, loc, spd, mass=mass)
            self.planets.add(planet)


