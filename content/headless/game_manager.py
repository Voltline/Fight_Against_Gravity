import math
from typing import List

from content.headless.objects import HShip, HPlanet, HBullet
from content.headless.vec2 import Vec2
from content.game_modules.physics import G


class HGameManager:
    def __init__(self, settings):
        self.settings = settings
        self.ships: List[HShip] = []
        self.dead_ships: List[HShip] = []
        self.planets: List[HPlanet] = []
        self.bullets: List[HBullet] = []
        self.center_v = Vec2()
        self.max_dis = 6e3

    def all_move(self, delta_t):
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
        del_ids = []
        for bullet in list(self.bullets):
            if bullet.check_del(self.planets, self.ships, self.center_v, self.max_dis):
                del_ids.append(bullet.id)
                self.bullets.remove(bullet)
        return del_ids

    def ships_check_far(self):
        for ship in list(self.ships):
            if ship.check_far(self.planets, self.max_dis) > 1:
                ship.die(self.ships, self.dead_ships, 0)

    def _circle_collision(self, obj1, r1, obj2, r2):
        diff = obj1.loc - obj2.loc
        return diff.dot(diff) <= (r1 + r2) ** 2

    def check_bullets_planets_collisions(self):
        collided = {}
        for bullet in list(self.bullets):
            for planet in self.planets:
                if self._circle_collision(bullet, bullet.radius, planet, planet.radius):
                    collided[bullet] = planet
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
        return collided

    def check_ships_bullets_collisions(self, time: float):
        collisions = {}
        for ship in list(self.ships):
            for bullet in list(self.bullets):
                if self._circle_collision(ship, self.settings.ship_radius, bullet, bullet.radius):
                    ship.die(self.ships, self.dead_ships, time)
                    collisions.setdefault(ship, []).append(bullet)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
        return collisions

    def check_ships_planets_collisions(self, time: float):
        collisions = {}
        for ship in list(self.ships):
            for planet in self.planets:
                if self._circle_collision(ship, self.settings.ship_radius, planet, planet.radius):
                    ship.die(self.ships, self.dead_ships, time)
                    collisions.setdefault(ship, []).append(planet)
        return collisions

    def check_ships_ships_collisions(self, time: float):
        collisions = {}
        for i, ship1 in enumerate(self.ships):
            for ship2 in self.ships[i + 1:]:
                if self._circle_collision(ship1, self.settings.ship_radius, ship2, self.settings.ship_radius):
                    ship1.die(self.ships, self.dead_ships, time)
                    ship2.die(self.ships, self.dead_ships, time)
                    collisions.setdefault(ship1, []).append(ship2)
                    collisions.setdefault(ship2, []).append(ship1)
        return collisions

    def check_collisions(self, time: float):
        self.check_ships_ships_collisions(time)
        self.check_ships_planets_collisions(time)
        self.check_ships_bullets_collisions(time)
        self.check_bullets_planets_collisions()

    def load_map(self, game_map, player_names):
        self.ships.clear()
        self.dead_ships.clear()
        self.planets.clear()
        self.bullets.clear()
        planets_info, ships_info = game_map.planets_info, game_map.ships_info

        def loc_spd(info):
            # 兼容 SpawnInfo/字典结构
            loc_val = info.loc if hasattr(info, "loc") else info.get("loc")
            spd_val = info.spd if hasattr(info, "spd") else info.get("spd")
            loc = Vec2(loc_val[0], loc_val[1])
            spd = Vec2(spd_val[0], spd_val[1])
            return loc, spd

        # ship 半径配置（近似原 mask 尺寸）
        self.ship_radius = getattr(self.settings, "ship_collision_radius",
                                   getattr(self.settings, "ship_radius", 80))

        for planet_info in planets_info:
            loc, spd = loc_spd(planet_info)
            mass = planet_info.mass if hasattr(planet_info, "mass") else planet_info["mass"]
            radius = None
            if hasattr(planet_info, "radius"):
                radius = planet_info.radius
            elif hasattr(planet_info, "size"):
                radius = planet_info.size
            else:
                radius = planet_info.get("radius", planet_info.get("size", 50))
            self.planets.append(HPlanet(self.settings, loc, spd, mass, radius))
        for i, ship_info in enumerate(ships_info):
            loc, spd = loc_spd(ship_info)
            angle = ship_info.angle if hasattr(ship_info, "angle") else ship_info["angle"]
            player_name = player_names[i] if i < len(player_names) else f"player_{i}"
            self.ships.append(HShip(self.settings, loc, spd, angle, player_name))

    def make_ships_msg(self):
        return [ship.make_msg() for ship in self.ships]

    def make_dead_players_name_msg(self):
        return [ship.player_name for ship in self.dead_ships]

    def make_dead_bullets_msg(self):
        return []

    def make_bullets_msg(self):
        return [bullet.make_msg() for bullet in self.bullets]
