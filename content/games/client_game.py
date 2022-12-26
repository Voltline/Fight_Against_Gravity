import math
import pygame
from pygame import Vector2

from content.games.online_game import OnlineGame
from content.local.camera import Camera
from Server.Modules.safeclient import SocketClient
from Server.Modules.OptType import OptType
import content.game_modules.game_function as gf
from content.online.snapshot import Snapshot
from content.online.obj_msg import ObjMsg
from content.game_modules.physics import is_close
from content.space_objs.ship import Ship
from content.space_objs.bullet import Bullet
from content.online.player_info import PlayerInfo


class ClientGame(OnlineGame):
    """客户端游戏"""
    def __init__(self, settings, net: SocketClient, room_id, map_name, player_names, screen, player_name):
        super().__init__(settings, screen, net, room_id, map_name, player_names)
        self.player_name = player_name
        self.player_ship = None  # 玩家的飞船
        self.camera = None
        self.traces = []
        self.snapshots = []  # 用于检查预测正确性的快照
        self.snapshots_len = settings.snapshots_len
        self.ping_ms = 0  # 延迟

        # 校时
        print('开始校时')
        self.lag_time = self.get_lag_time(room_id)
        print('校时成功,lag_time=', self.lag_time)  # TODO: debug

        self.last_all_ships_update_tick = 0
        self.last_bullets_update_tick = 0

    def restart(self):
        """重置状态到游戏开始"""
        super().restart()
        self.player_ship = gf.find_player_ship(self.gm.ships, self.player_name)
        self.camera = Camera(self.settings, self.screen, self.player_ship)
        self.traces = []
        self.snapshots.clear()
        self.snapshots.append(Snapshot(self.gm, self.now_tick))
        self.last_all_ships_update_tick = 0
        self.last_bullets_update_tick = 0

    def get_start_time(self) -> float:
        server_start_time = self.get_server_start_game_time(self.room_id)
        print('服务器游戏开始时间获取成功:', server_start_time)  # TODO: debug
        print(server_start_time - self.lag_time)
        return server_start_time - self.lag_time

    def get_lag_time(self, room_id):
        """
        校时：获取本地时钟比服务器落后多少秒
        方式：
            记录本地时间a并发送，
            服务器记录接收时间b再发送，
            本地记录接收时间c
            则lag_time = b-(a+c)/2
        """
        lag_time_sum = 0
        check_num = self.settings.net_clock_check_num
        for cnt in range(check_num):
            time_a = gf.get_time()
            msg = {
                'opt': OptType.CheckClock,
                'time': time_a,
                'args': [room_id, self.player_name],
                'kwargs': {}
            }
            self.net.send(msg)
            print('已发送校时信息:', cnt)  # TODO: debug
            msg = None
            while not msg:
                msg = self.net.receive()
                if msg:
                    if msg['opt'] == OptType.CheckClock:
                        if msg['args'][1] != self.player_name:
                            msg = None
                    else:
                        msg = None
            time_b = msg['time']
            time_c = gf.get_time()
            lag_time_sum += time_b - (time_a + time_c)/2
        return lag_time_sum/check_num

    def get_server_start_game_time(self, room_id):
        """等待直到获取服务器开始游戏的时间"""
        self.send_get_server_start_time_msg(room_id)
        msg = None
        while not msg:
            msg = self.net.receive()
            if msg['opt'] == OptType.ServerStartGameTime:
                if msg['args'][0] != room_id:
                    msg = None
            else:
                msg = None
        return msg['time']

    def send_get_server_start_time_msg(self, room_id):
        """发送向服务器请求开始游戏时间的消息"""
        msg = {
            'opt': OptType.ServerStartGameTime,
            'args': [room_id]
        }
        self.net.send(msg)

    def deal_event(self, event):
        """处理消息"""
        super().deal_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # 是否按下鼠标中键
                self.camera.change_mode()
            elif event.button == 1:  # 按下鼠标左键
                self.player_ship.is_fire = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 松开鼠标左键
                self.player_ship.is_fire = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[2]:  # 如果鼠标右键被按下
                self.camera.d_loc.update(self.mouse_d_loc)
        elif event.type == pygame.MOUSEWHEEL:
            self.camera.d_zoom = event.y

        elif event.type == pygame.KEYDOWN:
            self.check_events_keydown(event)
        elif event.type == pygame.KEYUP:
            self.check_events_keyup(event)

    def check_events_keydown(self, event):
        """处理按下按键"""
        if event.key == self.settings.ship1_k_go_ahead:
            self.player_ship.is_go_ahead = True
        elif event.key == self.settings.ship1_k_go_back:
            self.player_ship.is_go_back = True
        elif event.key == self.settings.ship1_k_turn_left:
            self.player_ship.is_turn_left = True
        elif event.key == self.settings.ship1_k_turn_right:
            self.player_ship.is_turn_right = True
        elif event.key == self.settings.ship1_k_fire:
            self.player_ship.is_fire = True

    def check_events_keyup(self, event):
        """处理松开按键"""
        if event.key == self.settings.ship1_k_go_ahead:
            self.player_ship.is_go_ahead = False
        elif event.key == self.settings.ship1_k_go_back:
            self.player_ship.is_go_back = False
        elif event.key == self.settings.ship1_k_turn_left:
            self.player_ship.is_turn_left = False
        elif event.key == self.settings.ship1_k_turn_right:
            self.player_ship.is_turn_right = False
        elif event.key == self.settings.ship1_k_fire:
            self.player_ship.is_fire = False

    def send_msgs_physic_loop(self):
        """发送玩家控制消息"""
        self.send_ctrl_msg()

    def deal_msgs_physic_loop(self):
        """接收并处理消息"""
        all_ships_msg = None
        all_ships_msg_tick = 0
        bullets_msg = None
        bullets_msg_tick = 0
        new_bullets_msg = None
        new_bullets_msg_tick = 0
        dead_bullets_msg = []
        for msg in self.net.get_message_list():
            opt = msg['opt']
            if 'time' in msg:
                time = msg['time']
            if 'tick' in msg:
                tick = msg['tick']
            if 'args' in msg:
                args = msg['args']
            if 'kwargs' in msg:
                kwargs = msg['kwargs']

            if tick > self.now_tick:  # 如果消息过新就塞回消息队列
                self.net.que.put(msg)
            elif opt == OptType.AllShips:
                if not all_ships_msg or all_ships_msg_tick < tick:
                    all_ships_msg_tick = tick
                    all_ships_msg = args
            elif opt == OptType.Bullets:
                if not bullets_msg or bullets_msg_tick < tick:
                    bullets_msg_tick = tick
                    bullets_msg = args
            elif opt == OptType.AddDelBullets:
                if not new_bullets_msg or new_bullets_msg_tick < tick:
                    new_bullets_msg_tick = tick
                    new_bullets_msg, dead_bullets_msg = args
                    self.add_bullets(new_bullets_msg, new_bullets_msg_tick)
                    self.del_bullets(dead_bullets_msg)

        if all_ships_msg:
            self.ping_ms = (self.now_tick-all_ships_msg_tick)*self.physics_dt*1000
            self.all_ships_update(all_ships_msg, all_ships_msg_tick)
        if bullets_msg:
            self.bullets_update(bullets_msg, bullets_msg_tick)

    def send_ctrl_msg(self):
        ctrl_msg = self.player_ship.make_ctrl_msg()
        msg = {
            'opt': OptType.PlayerCtrl,
            'tick': self.now_tick,
            'args': [self.room_id, self.player_name, ctrl_msg],
        }
        self.net.send(msg)

    def physic_update(self):
        """每个物理dt的更新行为"""
        super().physic_update()
        self.check_collisions()
        self.gm.all_move(self.physics_dt)
        self.update_snapshots()

    def physic_loop(self):
        """
        在基类的check_events之后要发送游戏是否结束等消息
        在基类的物理循环之后要添加尾迹
        """
        if not self.is_run:
            self.send_stop_game_msg(self.room_id, self.now_time)
        super().physic_loop()
        gf.add_traces(self.settings, self.gm, self.traces, self.now_time)

    def display(self):
        """更新屏幕"""
        surplus_ratio = self.surplus_dt / self.physics_dt
        self.camera.mouse_loc.update(self.mouse_loc)
        gf.update_screen(self.settings, self.gm, self.camera,
                         self.traces, surplus_ratio, self.now_time)

    def send_stop_game_msg(self, room_id, now_sec):
        """发送游戏停止信息"""
        msg = {
            'opt': OptType.StopGame,
            'time': now_sec,
            'args': [room_id],
            'kwargs': {}
        }
        self.net.send(msg)

    def update_snapshots(self):
        """把这个tick结束时的状态存入snapshots，把过于久远的状态删除"""
        self.snapshots.insert(0, Snapshot(self.gm, self.now_tick))
        while self.now_tick - self.snapshots[-1].tick >= self.snapshots_len:
            self.snapshots.pop()

    def update_problem_objs(self, all_objs: dict, tick: int) -> dict:
        """把出问题的objs从tick加载到now_tick"""
        planets = self.gm.planets
        planets_num = len(planets)
        i = self.get_snapshot_i(tick)
        ships = []
        bullets = pygame.sprite.Group()
        if 'ships' in all_objs:
            ships = all_objs['ships']
        if 'bullets' in all_objs:
            bullets.add(all_objs['bullets'])
        all_objs['dead_bullets_id'] = []

        if i > 0:
            for snapshot in self.snapshots[i-1::-1]:
                for dead_bullet in self.gm.static_check_bullets_planets_collisions(bullets, planets).keys():
                    all_objs['dead_bullets_id'].append(dead_bullet.id)
                i = 0
                for planet in planets:
                    planet.loc.update(snapshot.splanets[i].loc)
                    i += 1
                for ship in ships:
                    ship.move(self.physics_dt, planets)
                    snapshot.ships_loc[ship.player_name] = ship.loc.copy()
                    snapshot.ships_angle[ship.player_name] = ship.angle
                    snapshot.ships_hp[ship.player_name] = ship.hp
                    snapshot.ships_ctrl_msg[ship.player_name] = ship.make_ctrl_msg()
                for bullet in bullets:
                    bullet.move(self.physics_dt, planets)
                    snapshot.bullets_loc[bullet.id] = bullet.loc.copy()
        return all_objs

    def get_problem_ships(self, ships_msg: list, snapshot: Snapshot) -> list:
        """事先准备好同一个tick的ships_msg和snapshot_ships，返回位置偏差较大的对象"""
        problem_ships = []
        ships_loc = snapshot.ships_loc
        ships_angle = snapshot.ships_angle
        ships_hp = snapshot.ships_hp
        splanets = snapshot.splanets
        ships_ctrl_msg = snapshot.ships_ctrl_msg
        for ship_msg in ships_msg:
            msg = ObjMsg(msg=ship_msg)
            if not is_close(Vector2(msg.locx, msg.locy), ships_loc[msg.player_name])\
                    or not math.isclose(msg.angle, ships_angle[msg.player_name])\
                    or msg.hp != ships_hp[msg.player_name]\
                    or ships_ctrl_msg[msg.player_name] != msg.ctrl_msg:
                ship = Ship(self.settings, player_name=msg.player_name)
                ship.update_by_msg(ship_msg, splanets)
                problem_ships.append(ship)
        return problem_ships

    def get_problem_bullets(self, bullets_msg: list, snapshot: Snapshot) -> (list, list):
        """事先准备好同一个tick的bullets_msg和snapshot_bullets，返回位置偏差较大的对象"""
        problem_bullets = []
        bullets_loc = snapshot.bullets_loc
        splanets = snapshot.splanets
        for bullet_msg in bullets_msg:
            msg = ObjMsg(msg=bullet_msg)
            if msg.id not in bullets_loc or not is_close(Vector2(msg.locx, msg.locy), bullets_loc[msg.id]):
                bullet = Bullet(self.settings)
                bullet.update_by_msg(bullet_msg, splanets)
                problem_bullets.append(bullet)
        return problem_bullets

    def add_bullets(self, bullets_msg: list, tick):
        """根据new_bullets_msg添加子弹"""
        bullets = []

        for bullet_msg in bullets_msg:
            bullet = Bullet(self.settings)
            bullet.update_by_msg(bullet_msg,
                self.snapshots[self.get_snapshot_i(tick)].splanets)
            bullets.append(bullet)
        all_objs = {'bullets': bullets}
        self.update_problem_objs(all_objs, tick)
        for new_bullet in bullets:
            for bullet in self.gm.bullets:
                if bullet.id == new_bullet.id:
                    bullet.copy(new_bullet)
                    break
            else:
                self.gm.bullets.add(new_bullet)

    def del_bullets(self, bullets_id: list):
        """根据dead_bullets_msg删除子弹，不需要预测"""
        for bullet_id in bullets_id:
            for bullet in self.gm.bullets:
                if bullet.id == bullet_id:
                    self.gm.bullets.remove(bullet)
                    break

    def get_snapshot_i(self, tick):
        """获取tick对应的snapshot在snapshots中的下标"""
        if tick < self.snapshots[-1].tick:  # 太古老
            return -1
        elif tick > self.now_tick:  # 太新
            return 0
        else:
            return self.now_tick - tick

    def ships_die(self, dead_players_name: list, dead_time: float):
        """根据消息让死亡的玩家死亡"""
        for name in dead_players_name:
            for ship in self.gm.ships:
                if name == ship.player_name:
                    ship.die(self.gm.ships, self.gm.dead_ships, dead_time)
                    break

    def all_ships_update(self, all_ship_msg, tick):
        """根据消息进行回滚、比较、重预测"""
        if tick > self.last_all_ships_update_tick:
            self.last_all_ships_update_tick = tick
            ships_msg, dead_players_name = all_ship_msg
            self.ships_die(dead_players_name, tick*self.physics_dt)
            si = self.get_snapshot_i(tick)
            ships = self.get_problem_ships(ships_msg, self.snapshots[si])
            all_objs = {'ships': ships}
            self.update_problem_objs(all_objs, tick)
            for pro_ship in ships:
                for ship in self.gm.ships:
                    if ship.player_name == pro_ship.player_name:
                        if ship.player_name == PlayerInfo.player_name:
                            ship.copy(pro_ship, False)
                        else:
                            ship.copy(pro_ship)
                        break

    def bullets_update(self, bullets_msg, tick):
        """根据消息进行回滚、比较、重预测"""
        if tick > self.last_bullets_update_tick:
            self.last_bullets_update_tick = tick

            si = self.get_snapshot_i(tick)
            bullets = self.get_problem_bullets(bullets_msg, self.snapshots[si])
            all_objs = {'bullets': bullets}
            self.update_problem_objs(all_objs, tick)
            for pro_bullet in bullets:
                for bullet in self.gm.bullets:
                    if pro_bullet.id == bullet.id:
                        bullet.copy(pro_bullet)
                        break
                else:
                    self.gm.bullets.add(pro_bullet)

    def check_collisions(self):
        """只检查子弹和星球"""
        self.gm.check_bullets_planets_collisions()

    def print_debug(self):
        """输出调试信息"""
        print('ping_ms:', self.ping_ms)
        super().print_debug()
