import pygame
from pygame import Vector2

from online_game import OnlineGame
from content.maps.map_obj import Map
from content.game_manager import GameManager
from content.camera import Camera
from Web.Modules.OptType import OptType
import content.game_function as gf


class ClientGame(OnlineGame):
    """客户端游戏"""
    def __init__(self, settings, net, room_id, map_name, player_names, screen, player_name):
        super().__init__(settings, net, room_id, map_name, player_names)
        self.screen = screen
        self.player_name = player_name
        self.player_ship = None  # 玩家的飞船
        self.camera = None
        self.traces = []

        # 校时
        print('开始校时')
        self.lag_time = self.get_lag_time(room_id)
        print('校时成功,lag_time=', self.lag_time, '开始获取游戏开始时间')  # TODO: debug

    def restart(self):
        """重置状态到游戏开始"""
        super().restart()
        self.player_ship = gf.find_player_ship(self.gm.ships, self.player_name)
        self.camera = Camera(self.screen, self.settings, self.player_ship)
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
            则lag_time = (a+c)/2-b
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
            if msg:
                if msg['opt'] == OptType.ServerStartGameTime:
                    if msg['args'][0] != room_id:
                        msg = None
                else:
                    msg = None
        return msg['time']
