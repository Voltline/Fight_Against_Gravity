from settings.all_settings import Settings
from content.game import game_function as gf
from content.online.player_info import PlayerInfo
from Server.Modules.safeclient import SocketClient
from content.online.client_game import ClientGame
import os


class Client:
    """客户端"""
    ip = '1.15.229.11'
    port = 25555

    def __init__(self):
        self.net = SocketClient(Client.ip, Client.port, msg_len=1048576)  # 负责收发信息
        path = os.path.dirname(os.path.realpath(__file__)) + '\\'
        self.settings = Settings(path)  # 初始化设置类
        del path
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
