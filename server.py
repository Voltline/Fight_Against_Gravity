import threading
import pygame

from all_settings import Settings
from Web.Modules.OptType import OptType
from Web.Modules.safeserver import SocketServer
from game_room import GameRoom


class Server:
    """服务端"""
    ip = '10.0.4.17'
    port = 25555

    def __init__(self):
        self.net = SocketServer(Server.ip, Server.port)  # 负责收发信息
        self.settings = Settings()  # 初始化设置类
        self.rooms = {}  # {id(int): game_room}
        self.threads = {}  # {id(int): room_thread}

    def main(self):
        """服务端主函数"""
        # 开启一局游戏的步骤：
        # 房主点击开始游戏按钮，服务器收集{房间id,所有玩家id,地图名字}并调用创建游戏函数
        # 模拟时收集信息步骤省略
        self.net.start()
        clock = pygame.time.Clock()  # 准备时钟

        # 不断接收消息
        is_run = [True]
        while is_run[0]:
            clock.tick(self.settings.max_fps)
            self.deal_msg()

    def deal_msg(self):
        """接收并处理消息"""
        messages = self.net.get_message()
        for address, msg in messages:
            print(address, msg)
            mopt = msg['opt']
            if msg['time']:
                time = msg['time']
            if msg['args']:
                args = msg['args']
            if msg['kwargs']:
                kwargs = msg['kwargs']

            if mopt == OptType.StartGame:
                room_id, map_name, player_names = args
                self.start_game(room_id, map_name, player_names)
            elif mopt == OptType.StopGame:
                room_id = args[0]
                self.rooms[room_id].is_run[0] = False
            elif mopt == OptType.PlayerCtrl:
                room_id, player_name, ctrl_msg = args
                self.rooms[room_id].load_ctrl_msg(player_name, ctrl_msg)
            elif mopt == OptType.CheckClock:
                room_id, player_name = args
                self.rooms[room_id].send_check_clock_msg(player_name, address)

    def start_game(self, room_id, map_name, player_names):
        """开始一局新的room_game"""
        print('开始start_game')  # TODO: debug
        new_room = GameRoom(self.settings, self.net, room_id, map_name, player_names)
        new_thread = threading.Thread(target=new_room.main)
        self.rooms[room_id] = new_room
        self.threads[room_id] = new_thread
        new_thread.start()
        print('结束start_game')  # TODO: debug


if __name__ == '__main__':
    server = Server()
    server.main()
