import math
from typing import List, Dict

from content.headless.vec2 import Vec2
from content.online.obj_msg import ObjMsg
from content.game_modules.physics import gvt_acc, G


class HSpaceObj:
    def __init__(self, settings, loc0=None, spd0=None):
        self.loc: Vec2 = loc0.copy() if loc0 else Vec2()
        self.loc0: Vec2 = self.loc.copy()
        self.spd: Vec2 = spd0.copy() if spd0 else Vec2()
        self.acc: Vec2 = Vec2()

    def get_acc_from_planets(self, planets: List["HPlanet"]) -> Vec2:
        acc = Vec2()
        for planet in planets:
            acc += gvt_acc(planet.mass, planet.loc, self.loc)
        return acc

    def update_acc(self, planets) -> Vec2:
        acc0 = self.acc
        self.acc = self.get_acc_from_planets(planets)
        return acc0

    def update_loc(self, dt):
        self.loc0.update(self.loc)
        self.loc = self.loc + self.spd * dt + self.acc * (dt * dt / 2)

    def update_loc_spd(self, dt, planets):
        acc0 = self.acc
        self.update_loc(dt)
        self.update_acc(planets)
        self.spd = self.spd + (acc0 + self.acc) * (dt / 2)

    def move(self, delta_t, planets):
        self.update_loc_spd(delta_t, planets)

    def make_msg(self):
        return ObjMsg(self).make_msg()

    def update_by_msg(self, msg, planets):
        obj = ObjMsg(msg=msg)
        self.loc = Vec2(obj.locx, obj.locy)
        self.spd = Vec2(obj.spdx, obj.spdy)
        self.update_acc(planets)

    def get_ep_d_m(self, planets):
        epdm = 0
        for planet in planets:
            if self is not planet:
                diff = self.loc - planet.loc
                epdm -= G * planet.mass / (math.hypot(diff.x, diff.y))
        return epdm

    def get_ek_d_m(self, center_v: Vec2):
        dv = self.spd - center_v
        return 0.5 * dv.dot(dv)


class HPlanet(HSpaceObj):
    def __init__(self, settings, loc0=None, spd0=None, mass=1.0, radius=50):
        super().__init__(settings, loc0, spd0)
        self.mass = mass
        self.radius = radius
        self.acc0 = Vec2()

    def update_acc(self, planets):
        acc0 = self.acc.copy()
        self.acc = self.get_acc_from_planets(planets)
        return acc0

    def update_loc(self, dt):
        self.loc0.update(self.loc)
        self.loc = self.loc + self.spd * dt + self.acc * (dt * dt / 2)

    def update_spd(self, dt):
        self.spd = self.spd + (self.acc0 + self.acc) * (dt / 2)

    def update_loc_spd(self, dt, planets):
        self.acc0.update(self.acc)
        self.update_loc(dt)
        self.update_acc(planets)
        self.update_spd(dt)


class HBullet(HSpaceObj):
    COLOR = (0, 0, 0)
    next_id = 0

    def __init__(self, settings, loc0=None, spd0=None, bullet_id=-1):
        super().__init__(settings, loc0, spd0)
        self.radius = settings.bullet_radius
        self.damage = settings.bullet_damage
        self.id = HBullet.next_id if bullet_id < 0 else bullet_id
        HBullet.next_id = self.id + 1

    @staticmethod
    def init(settings):
        HBullet.COLOR = settings.bullet_color
        HBullet.next_id = 0

    def get_e_d_m(self, planets, center_v: Vec2):
        return self.get_ek_d_m(center_v) + self.get_ep_d_m(planets)

    def check_del(self, planets, ships, center_v: Vec2, max_dis: float) -> bool:
        min_dis = math.hypot(self.loc.x, self.loc.y)
        for objs in (planets, ships):
            for obj in objs:
                diff = self.loc - obj.loc
                dis = math.hypot(diff.x, diff.y)
                if (self.spd - obj.spd).dot(obj.loc - self.loc) > 0:
                    return False
                if dis < min_dis:
                    min_dis = dis
        edm = self.get_e_d_m(planets, center_v)
        if edm > 0 and min_dis > max_dis \
                or edm > -1e-5 and min_dis > max_dis * 2 \
                or edm > -1e-2 and min_dis > max_dis * 3 \
                or min_dis > max_dis * 4:
            return True
        return False

    def update_by_msg(self, msg, planets):
        super().update_by_msg(msg, planets)
        obj = ObjMsg(msg=msg)
        self.id = obj.id


class HShip(HSpaceObj):
    def __init__(self, settings, loc0=None, spd0=None, angle=0, player_name="?"):
        super().__init__(settings, loc0, spd0)
        self.angle = angle
        self.player_name = player_name
        self.hp = settings.ship_hp
        self.fire_heat = 0
        self.max_heat = 1
        self.d_fire_heat = 0.05
        self.d_cool_heat = 0.03
        self.go_acc = settings.ship_go_acc
        self.turn_spd = settings.ship_turn_spd
        self.is_go_ahead = False
        self.is_go_back = False
        self.is_turn_left = False
        self.is_turn_right = False
        self.is_fire = False
        self.is_alive = True

    def update_angle(self, delta_t):
        if self.is_turn_left:
            self.angle -= self.turn_spd * delta_t
        if self.is_turn_right:
            self.angle += self.turn_spd * delta_t

    def update_acc(self, planets):
        acc0 = self.acc
        self.acc = Vec2()
        if self.is_go_ahead:
            self.acc += Vec2(self.go_acc * math.cos(self.angle), self.go_acc * math.sin(self.angle))
        if self.is_go_back:
            self.acc -= Vec2(self.go_acc * math.cos(self.angle), self.go_acc * math.sin(self.angle))
        self.acc += self.get_acc_from_planets(planets)
        return acc0

    def move(self, delta_t, planets):
        self.update_angle(delta_t)
        self.update_loc_spd(delta_t, planets)

    def make_ctrl_msg(self):
        return [self.is_go_ahead, self.is_go_back, self.is_turn_left,
                self.is_turn_right, self.is_fire]

    def load_ctrl_msg(self, ctrl_msg):
        self.is_go_ahead, self.is_go_back, self.is_turn_left, \
            self.is_turn_right, self.is_fire = ctrl_msg

    def die(self, ships, dead_ships, time=0):
        self.is_alive = False
        self.hp = 0
        if self in ships:
            ships.remove(self)
        if self not in dead_ships:
            dead_ships.append(self)

    def check_far(self, planets, max_dis):
        dis = (self.loc - planets.sprites()[0].loc).length() if hasattr(planets, "sprites") else self.loc.length()
        if dis > max_dis:
            return 2
        return 0

    def load_ctrl_msg_and_heat(self, delta_t):
        if self.fire_heat < self.max_heat:
            self.fire_heat -= self.d_cool_heat * delta_t
        if self.is_fire and self.fire_heat + self.d_fire_heat <= self.max_heat:
            self.fire_heat += self.d_fire_heat
            return True
        return False
