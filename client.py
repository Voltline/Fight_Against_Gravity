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
from content.msg_type import MsgType
from Web.Modules.safeclient import SocketClient


class Client:
    """客户端"""
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

        # 鼠标位置信息，每帧实时更新
        self.mouse_loc = Vector2(0, 0)
        self.mouse_d_loc = Vector2(0, 0)

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
        player_names = ['player1']
        gf.button_start_game_click(self.net, room_id, map_name, player_names)
        print('开始游戏')
        # 游戏开始
        self.game(room_id, map_name, player_names)

    def game(self, room_id, map_name, player_names):
        """在线游戏，本地端的游戏函数"""
        gm = GameManager(self.settings)
        gm.load_map(Map(map_name), player_names)
        camera = Camera(self.screen, self.settings, PlayerInfo.player_name, gm.ships)
        traces = []

        clock = pygame.time.Clock()  # 准备时钟
        printed_sec = 0  # 测试用，上次输出调试信息的时间
        sended_sec = 0  # 上次发送ctrlmsg的时间
        physics_dt = self.settings.physics_dt
        surplus_dt = 0  # 这次delta_t被physics_dt消耗剩下的时间

        # 校时
        print('开始校时')
        lag_time = self.get_lag_time(room_id)
        print('校时成功,lag_time=', lag_time, '开始获取游戏开始时间')  # TODO: debug
        server_start_time = self.get_server_start_game_time(room_id)
        print('游戏开始时间获取成功:', server_start_time)  # TODO: debug
        start_time = server_start_time - lag_time
        surplus_dt += gf.get_time() - start_time

        is_run = [True]
        while is_run[0]:
            delta_t = clock.tick(self.settings.max_fps) / 1000  # 获取delta_time(sec)并限制最大帧率
            now_sec = gf.get_time()  # 测试用，当前时间
            if now_sec - printed_sec > 2:  # 每2秒输出一次fps等信息
                printed_sec = now_sec
                print('fps:', clock.get_fps())
                print('飞船信息:')
                for ship in gm.ships:
                    print('\t', ship.player_name, ':', ship.hp, ship.loc, ship.spd.length())
                print('子弹总数:', len(gm.bullets))

            ctrl_msg0 = gf.find_player_ship(gm.ships, PlayerInfo.player_name).make_ctrl_msg()
            self.check_events(gm, camera, is_run)  # 检查键鼠活动
            if ctrl_msg0 != gf.find_player_ship(gm.ships, PlayerInfo.player_name).make_ctrl_msg():  # 每0.1s发一次ctrlmsg
                self.send_ctrl_msg(gm, room_id, now_sec)  # 发送控制消息

            surplus_dt += delta_t
            while surplus_dt >= physics_dt:
                surplus_dt -= physics_dt
                # gf.check_collisions(gm)
                gm.all_move(physics_dt)
                # gf.ships_fire_bullet(settings, gm)

            self.deal_msg(gm)  # 接收并处理消息
            if not is_run[0]:  # 如果游戏结束
                self.send_stop_game_msg(room_id, now_sec)

            gf.add_traces(self.settings, gm, traces, now_sec*1000)

            surplus_ratio = surplus_dt / physics_dt
            gf.update_screen(self.settings, gm, camera, traces, surplus_ratio)

    def send_ctrl_msg(self, gm, room_id, now_sec):
        """发送玩家控制消息"""
        ship = gf.find_player_ship(gm.ships, PlayerInfo.player_name)
        ctrl_msg = ship.make_ctrl_msg()
        msg = {
            'type': MsgType.PlayerCtrl,
            'time': now_sec,
            'args': [room_id, PlayerInfo.player_name, ctrl_msg],
            'kwargs': {}
        }
        self.net.send(msg)

    def send_stop_game_msg(self, room_id, now_sec):
        msg = {
            'type': MsgType.StopGame,
            'time': now_sec,
            'args': [room_id],
            'kwargs': {}
        }
        self.net.send(msg)

    def deal_msg(self, gm):
        """接收并处理消息"""
        print('开始接收消息')
        msg = self.net.receive()
        print('开始处理消息')
        if msg:
            mtype = msg['type']
            if msg['time']:
                time = msg['time']
            if msg['args']:
                args = msg['args']
            if msg['kwargs']:
                kwargs = msg['kwargs']

            if mtype == MsgType.AllObjs:
                gm.client_update(args[0], args[1], args[2])
            elif mtype == MsgType.Planets:
                gm.client_update(planets_msg=args[0])
            elif mtype == MsgType.AllShips:
                gm.client_update(all_ships_msg=args)
            elif mtype == MsgType.Bullets:
                gm.client_update(bullets_msg=args[0])
        print('结束处理消息')

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
                'type': MsgType.CheckClock,
                'time': time_a,
                'args': [room_id, PlayerInfo.player_name],
                'kwargs': {}
            }
            self.net.send(msg)
            print('已发送校时信息:', cnt)  # TODO: debug
            msg = None
            while not msg:
                msg = self.net.receive()
                if msg:
                    if msg['type'] == MsgType.CheckClock:
                        if msg['args'][1] != PlayerInfo.player_name:
                            msg = None
                    else:
                        msg = None
            time_b = msg['time']
            time_c = gf.get_time()
            lag_time_sum += (time_a + time_c)/2 - time_b
        return lag_time_sum/check_num

    def get_server_start_game_time(self, room_id):
        """获取服务器开始游戏的时间"""
        msg = None
        while not msg:
            msg = self.net.receive()
            if msg:
                if msg['type'] == MsgType.ServerStartGameTime:
                    if msg['args'][0] != room_id:
                        msg = None
                else:
                    msg = None
        return msg['time']

    def check_events(self, gm, camera, is_run):
        """响应键盘和鼠标事件"""
        self.mouse_loc.update(pygame.mouse.get_pos())
        self.mouse_d_loc.update(pygame.mouse.get_rel())
        camera.mouse_loc.update(self.mouse_loc)

        event = pygame.event.poll()
        while event:
            if event.type == pygame.QUIT:
                is_run[0] = False
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # 是否按下鼠标中键
                    camera.change_mode()
            elif event.type == pygame.MOUSEMOTION:
                mouse_keys = pygame.mouse.get_pressed()
                if mouse_keys[2]:  # 如果鼠标右键被按下
                    camera.d_loc.update(self.mouse_d_loc)
            elif event.type == pygame.MOUSEWHEEL:
                camera.d_zoom = event.y

            elif event.type == pygame.KEYDOWN:
                self.check_events_keydown(event, gm, is_run)
            elif event.type == pygame.KEYUP:
                self.check_events_keyup(event, gm)

            event = pygame.event.poll()

    def check_events_keydown(self, event, gm, is_run):
        """处理按下按键"""
        # 寻找玩家飞船
        player_ship = None
        for ship in gm.ships:
            if ship.player_name == PlayerInfo.player_name:
                player_ship = ship
                break

        if event.key == self.settings.ship1_k_go_ahead:
            player_ship.is_go_ahead = True
        elif event.key == self.settings.ship1_k_go_back:
            player_ship.is_go_back = True
        elif event.key == self.settings.ship1_k_turn_left:
            player_ship.is_turn_left = True
        elif event.key == self.settings.ship1_k_turn_right:
            player_ship.is_turn_right = True
        elif event.key == self.settings.ship1_k_fire:
            player_ship.is_fire = True

        elif event.key == pygame.K_ESCAPE:  # TODO:暂定退出game按键为Esc
            is_run[0] = False

    def check_events_keyup(self, event, gm):
        """处理松开按键"""
        # 寻找玩家飞船
        player_ship = None
        for ship in gm.ships:
            if ship.player_name == PlayerInfo.player_name:
                player_ship = ship
                break

        if event.key == self.settings.ship1_k_go_ahead:
            player_ship.is_go_ahead = False
        elif event.key == self.settings.ship1_k_go_back:
            player_ship.is_go_back = False
        elif event.key == self.settings.ship1_k_turn_left:
            player_ship.is_turn_left = False
        elif event.key == self.settings.ship1_k_turn_right:
            player_ship.is_turn_right = False
        elif event.key == self.settings.ship1_k_fire:
            player_ship.is_fire = False


if __name__ == '__main__':
    client = Client()
    client.main()
