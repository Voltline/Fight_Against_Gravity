import pygame

from online_game import OnlineGame
from content.camera import Camera
from Web.Modules.safeclient import SocketClient
from Web.Modules.OptType import OptType
import content.game_function as gf


class ClientGame(OnlineGame):
    """客户端游戏"""
    def __init__(self, settings, net: SocketClient, room_id, map_name, player_names, screen, player_name):
        super().__init__(settings, screen, net, room_id, map_name, player_names)
        self.player_name = player_name
        self.player_ship = None  # 玩家的飞船
        self.camera = None
        self.traces = []

        # 校时
        print('开始校时')
        self.lag_time = self.get_lag_time(room_id)
        print('校时成功,lag_time=', self.lag_time)  # TODO: debug

    def restart(self):
        """重置状态到游戏开始"""
        super().restart()
        self.player_ship = gf.find_player_ship(self.gm.ships, self.player_name)
        self.camera = Camera(self.settings, self.screen, self.player_ship)
        self.traces = []

    def get_start_time(self) -> float:
        server_start_time = self.get_server_start_game_time(self.room_id)
        print('服务器游戏开始时间获取成功:', server_start_time)  # TODO: debug
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
        msg = None
        while not msg:
            msg = self.net.receive()
            if msg['opt'] == OptType.ServerStartGameTime:
                if msg['args'][0] != room_id:
                    msg = None
            else:
                msg = None
        return msg['time']

    def events_loop(self):
        """更新消息的循环"""
        self.camera.mouse_loc.update(self.mouse_loc)
        super().events_loop()

    def deal_event(self, event):
        """处理消息"""
        super().deal_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # 是否按下鼠标中键
                self.camera.change_mode()
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

        elif event.key == pygame.K_ESCAPE:  # TODO:暂定退出game按键为Esc
            self.is_run = False

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

    def send_msg(self):
        """发送玩家控制消息"""
        ctrl_msg = self.player_ship.make_ctrl_msg()
        msg = {
            'opt': OptType.PlayerCtrl,
            'tick': self.now_tick,
            'args': [self.room_id, self.player_name, ctrl_msg],
        }
        self.net.send(msg)

    def deal_msgs(self):
        """接收并处理消息"""
        planets_msg = None
        planets_msg_tick = 0
        all_ships_msg = None
        all_ships_msg_tick = 0
        bullets_msg = None
        bullets_msg_tick = 0
        msg = self.net.get_message()
        while msg:
            opt = msg['opt']
            if 'time' in msg:
                time = msg['time']
            if 'tick' in msg:
                tick = msg['tick']
            if 'args' in msg:
                args = msg['args']
            if 'kwargs' in msg:
                kwargs = msg['kwargs']

            if opt == OptType.AllObjs:
                if not planets_msg or planets_msg_tick < tick:
                    planets_msg_tick = tick
                    planets_msg = args[0]
                if not all_ships_msg or all_ships_msg_tick < tick:
                    all_ships_msg_tick = tick
                    all_ships_msg = args[1]
                if not bullets_msg or bullets_msg_tick < tick:
                    bullets_msg_tick = tick
                    bullets_msg = args[2]
            elif opt == OptType.Planets:
                if not planets_msg or planets_msg_tick < tick:
                    planets_msg_tick = tick
                    planets_msg = args
            elif opt == OptType.AllShips:
                if not all_ships_msg or all_ships_msg_tick < tick:
                    all_ships_msg_tick = tick
                    all_ships_msg = args
            elif opt == OptType.Bullets:
                if not bullets_msg or bullets_msg_tick < tick:
                    bullets_msg_tick = tick
                    bullets_msg = args

            msg = self.net.get_message()

        self.gm.client_update(planets_msg=planets_msg, tick=planets_msg_tick)
        self.gm.client_update(all_ships_msg=all_ships_msg, tick=all_ships_msg_tick)
        self.gm.client_update(bullets_msg=bullets_msg, tick=bullets_msg_tick)

    def physic_update(self):
        """每个物理dt的更新行为"""
        super().physic_update()
        self.gm.all_move(self.physics_dt)

    def physic_loop(self):
        """
        在基类的check_events之后要发送游戏是否结束等消息
        在基类的物理循环之后要添加尾迹
        """
        if not self.is_run:
            self.send_stop_game_msg(self.room_id, self.now_time)
        super().physic_loop()
        gf.add_traces(self.settings, self.gm, self.traces, self.now_time*1000)

    def display(self):
        """更新屏幕"""
        surplus_ratio = self.surplus_dt / self.physics_dt
        gf.update_screen(self.settings, self.gm, self.camera, self.traces, surplus_ratio)

    def send_stop_game_msg(self, room_id, now_sec):
        msg = {
            'opt': OptType.StopGame,
            'time': now_sec,
            'args': [room_id],
            'kwargs': {}
        }
        self.net.send(msg)
