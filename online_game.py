import pygame
from pygame import Vector2
from typing import Union

from content.maps.map_obj import Map
from content.game_manager import GameManager
import content.game_function as gf
from Web.Modules.safeserver import SocketServer
from Web.Modules.safeclient import SocketClient
from fag_game import FAGGame


class OnlineGame(FAGGame):
    """在线游戏，作为基类使用"""
    def __init__(self, settings, screen, net: Union[SocketServer, SocketClient], room_id, map_name, player_names):
        super().__init__(settings, screen, map_name, player_names)
        self.net = net
        self.room_id = room_id

        self.sended_tick = 0  # 上次广播消息的时间

    def restart(self):
        """重置状态到游戏开始"""
        super().restart()
        self.sended_tick = 0

    def physic_loop(self):
        """物理dt更新的循环，在线游戏每次物理循环之前先收发、处理消息"""
        self.send_msgs_main_loop()
        super().physic_loop()

    def physic_update(self):
        """每个物理dt的更新行为"""
        self.send_msgs_physic_loop()
        self.deal_msgs_physic_loop()
        super().physic_update()

    def send_msgs_main_loop(self):
        """main_loop中发送消息"""
        pass

    def send_msgs_physic_loop(self):
        """physic_loop中发送消息"""
        pass

    def deal_msgs_physic_loop(self):
        """physic_loop中接收并处理消息"""
        pass
