import time
import pygame
from pygame import Vector2
import sys

from content.game_manager import GameManager
from content.maps.map_obj import Map
from content.camera import Camera
from Web.Modules.OptType import OptType
from Web.Modules.safeserver import SocketServer
import content.game_function as gf


class GameRoom:
    """服务端的游戏房间"""
    def __init__(self, settings, net: SocketServer, room_id, map_name, player_names):
        self.settings = settings
        self.net = net
        self.id = room_id
        self.map_name = map_name
        self.map = Map(map_name)
        self.player_names = player_names
        self.gm = GameManager(self.settings)
        self.screen = None
        self.addresses = {}  # {player_name: address}
        self.is_run = [True]

        # 鼠标位置信息，每帧实时更新
        self.mouse_loc = Vector2(0, 0)
        self.mouse_d_loc = Vector2(0, 0)

    def main(self):
        """开始游戏"""
        pygame.init()
        icon = pygame.image.load(self.settings.icon_img_path)
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # 设置窗口大小
        pygame.display.set_caption(self.settings.game_title)  # 设置窗口标题

        self.gm.load_map(self.map, self.player_names)
        camera = Camera(self.settings, self.screen)
        traces = []

        clock = pygame.time.Clock()  # 准备时钟
        sended_sec = 0  # 上次广播消息的时间
        printed_sec = 0  # 测试用，上次输出调试信息的时间
        physics_dt = self.settings.physics_dt
        surplus_dt = 0  # 这次delta_t被physics_dt消耗剩下的时间

        print('开始校时')
        # 校时并确定每个player对应的address
        while len(self.addresses) != len(self.player_names):
            # print(self.addresses)
            pass
        print('完成校时')
        time.sleep(5)
        print('开始发送游戏开始时间')
        self.send_start_game_time(gf.get_time()+3)  # 等3秒之后开始游戏
        print('游戏开始时间发送成功')
        surplus_dt -= 3

        while self.is_run[0]:
            delta_t = clock.tick(self.settings.max_fps) / 1000  # 获取delta_time(sec)并限制最大帧率
            now_sec = gf.get_time()  # 测试用，当前时间
            if now_sec - printed_sec >= 2:  # 每2秒输出一次fps等信息
                printed_sec = now_sec
                print('fps:', clock.get_fps())
                print('飞船信息:')
                for ship in self.gm.ships:
                    print('\t', ship.player_name, ':', ship.hp, ship.loc, ship.spd.length())
                print('子弹总数:', len(self.gm.bullets))

            self.check_events(camera, self.is_run)
            # 在server.main更新玩家操作状态

            surplus_dt += delta_t
            while surplus_dt >= physics_dt:
                surplus_dt -= physics_dt
                self.gm.check_collisions()
                self.gm.all_move(physics_dt)
                self.gm.ships_fire_bullet()

            # 向房间所有玩家广播当前gm最新状态
            if now_sec - sended_sec > 0.01:
                sended_sec = now_sec
                self.send_gm_msg()

            # gf.add_traces(self.settings, self.gm, traces, now_sec*1000)

            surplus_ratio = surplus_dt / physics_dt
            gf.update_screen(self.settings, self.gm, camera, traces, surplus_ratio)

    def send_all(self, msg: dict):
        """向所有玩家广播msg"""
        for address in self.addresses.values():
            self.net.send(address, msg)

    def send_start_game_time(self, start_time):
        """向所有玩家广播游戏开始时间"""
        msg = {
            'opt': OptType.ServerStartGameTime,
            'time': start_time,
            'args': [self.id],
            'kwargs': {}
        }
        self.send_all(msg)

    def send_gm_msg(self):
        """
        向房间所有玩家广播当前gm最新状态
        分开发送，避免数据包过长
        """
        now_time = gf.get_time()
        # 广播planets
        msg = {
            'opt': OptType.Planets,
            'time': now_time,
            'args': self.gm.make_planets_msg()
        }
        self.send_all(msg)

        # 广播all_ships
        msg = {
            'opt': OptType.AllShips,
            'time': now_time,
            'args': [self.gm.make_ships_msg(), self.gm.make_dead_players_name_msg()]
        }
        self.send_all(msg)

        # 广播bullets
        msg = {
            'opt': OptType.Bullets,
            'time': now_time,
            'args': self.gm.make_bullets_msg()
        }
        self.send_all(msg)

    def load_ctrl_msg(self, player_name, ctrl_msg):
        """加载操作信息"""
        ship = gf.find_player_ship(self.gm.ships, player_name)
        ship.load_ctrl_msg(ctrl_msg)

    def send_check_clock_msg(self, player_name, addr):
        """对玩家发送校时消息"""
        self.addresses[player_name] = addr

        msg = {
            'opt': OptType.CheckClock,
            'time': gf.get_time(),
            'args': [self.id, player_name],
            'kwargs': {}
        }
        self.net.send(self.addresses[player_name], msg)

    def check_events(self, camera, is_run):
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

            event = pygame.event.poll()
