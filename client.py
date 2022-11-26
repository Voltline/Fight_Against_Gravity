from Web.Modules.safeclient import SocketClient
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
from content.msg_type import MsgType


class Client:
    ip = '1.15.229.11'
    port = 25555

    def __init__(self):
        self.net = SocketClient(Client.ip, Client.port)  # 负责收发信息
        self.settings = Settings()  # 初始化设置类
        pygame.init()
        icon = pygame.image.load(self.settings.icon_img_path)
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # 设置窗口大小
        pygame.display.set_caption(self.settings.game_title)  # 设置窗口标题

    def main(self):
        """客户端主函数"""
        # 开启一局游戏的步骤：
        # 房主点击开始游戏按钮，服务器收集{房间id,所有玩家id,地图名字}并调用创建游戏函数
        # 模拟时收集信息步骤省略

        # 登陆账号
        PlayerInfo.player_name = 'player1'

        # 在房间中，点击开始游戏按钮
        room_id = 1
        map_name = '静止双星系统'
        player_names = ['player1', 'player2']
        gf.button_start_game_click(self.net, room_id, map_name, player_names)

        # 游戏开始
        self.client_game(room_id, map_name, player_names)

    def client_game(self, room_id, map_name, player_names):
        """在线游戏，本地端的游戏函数"""
        gm = GameManager(self.settings)
        gm.load_map(Map(map_name), player_names)
        camera = Camera(self.screen, self.settings, PlayerInfo.player_name, gm.ships)
        traces = []

        clock = pygame.time.Clock()  # 准备时钟
        printed_ms = 0  # 测试用，上次输出调试信息的时间
        physics_dt = self.settings.physics_dt
        surplus_dt = 0  # 这次delta_t被physics_dt消耗剩下的时间

        is_run = [True]
        while is_run[0]:
            delta_t = clock.tick(self.settings.max_fps) / 1000  # 获取delta_time(sec)并限制最大帧率
            now_ms = pygame.time.get_ticks()  # 测试用，当前时间
            if now_ms - printed_ms >= 2000:  # 每2秒输出一次fps等信息
                printed_ms = now_ms
                print('fps:', clock.get_fps())
                print('飞船信息:')
                for ship in gm.ships:
                    print('\t', ship.player_name, ':', ship.hp, ship.loc, ship.spd.length())
                print('子弹总数:', len(gm.bullets))

            gf.check_events(self.settings, gm, camera, is_run)  # 检查键鼠活动

            surplus_dt += delta_t
            while surplus_dt >= physics_dt:
                surplus_dt -= physics_dt
                # gf.check_collisions(gm)
                gm.all_move(physics_dt)
                # gf.ships_fire_bullet(settings, gm)

            self.net.send(gm)  # 发送玩家控制消息
            self.deal_msg(gm)  # 接收并处理消息

            gf.add_traces(self.settings, gm, traces, now_ms)

            surplus_ratio = surplus_dt / physics_dt
            gf.update_screen(self.settings, gm, camera, traces, surplus_ratio)

    def send_ctrl_msg(self, gm):
        """发送玩家控制消息"""
        ctrl_msg = []
        for ship in gm.ships:
            if ship.player_name == PlayerInfo.player_name:
                ctrl_msg = ship.make_ctrl_msg()
                break
        msg = {
            'type': MsgType.PlayerCtrl,
            'args': ctrl_msg,
            'kwargs': {}
        }
        self.net.send(msg)

    def deal_msg(self, gm):
        """接收并处理消息"""
        msg = self.net.receive()
        if msg:
            msg_type = msg['type']
            args = msg['args']
            kwargs = msg['kwargs']
            if msg_type == MsgType.AllObjs:
                gm.client_update(args[0], args[1], args[2])
            elif msg_type == MsgType.Planets:
                gm.client_update(planets_msg=args[0])
            elif msg_type == MsgType.AllShips:
                gm.client_update(all_ships_msg=args)
            elif msg_type == MsgType.Bullets:
                gm.client_update(bullets_msg=args[0])


if __name__ == '__main__':
    client = Client()
    client.main()
