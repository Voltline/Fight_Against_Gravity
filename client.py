import sys
import pygame
from pygame import Vector2

from all_settings import Settings
from content import game_function as gf
from content.game_manager import GameManager
from content.ship import Ship
from content.planet import Planet
from content.camera import Camera
from content.maps.map_obj import Map
from content.player_info import PlayerInfo
from Web.Modules.OptType import OptType
from Web.Modules.safeclient import SocketClient
from client_game import ClientGame


class Client:
    """客户端"""
    ip = '1.15.229.11'
    port = 25555

    def __init__(self):
        self.net = SocketClient(Client.ip, Client.port, msg_len=1048576)  # 负责收发信息
        self.settings = Settings()  # 初始化设置类
        self.screen = gf.init_pygame_window(self.settings)
        self.game = ClientGame

    def main(self):
        """客户端主函数"""
        # 开启一局游戏的步骤：
        # 房主点击开始游戏按钮，服务器收集{房间id,所有玩家id,地图名字}并调用创建游戏函数
        # 模拟时收集信息步骤省略

        # 登陆账号
        PlayerInfo.player_name = 'player1'

        # 在房间中，点击开始游戏按钮
        room_id = 1
        map_name = '地月系统'
        player_names = ['player1']
        gf.button_start_game_click(self.net, room_id, map_name, player_names)
        print('开始游戏')
        # 游戏开始
        self.game =\
            ClientGame(self.settings, self.net, room_id, map_name,
                       player_names, self.screen, PlayerInfo.player_name)
        self.game.main()


if __name__ == '__main__':
    client = Client()
    client.main()
