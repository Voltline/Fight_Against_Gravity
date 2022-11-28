import time
import pygame

from content.game_manager import GameManager
from content.maps.map_obj import Map
from content.camera import Camera
from content.msg_type import MsgType
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
        self.players_address = {}  # {player_name: address}
        self.is_run = [True]

    def main(self):
        """开始游戏"""
        pygame.init()
        icon = pygame.image.load(self.settings.icon_img_path)
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # 设置窗口大小
        pygame.display.set_caption(self.settings.game_title)  # 设置窗口标题

        self.gm.load_map(self.map, self.player_names)
        camera = Camera(self.screen, self.settings, None, self.gm.ships)
        traces = []

        clock = pygame.time.Clock()  # 准备时钟
        printed_ms = 0  # 测试用，上次输出调试信息的时间
        physics_dt = self.settings.physics_dt
        surplus_dt = 0  # 这次delta_t被physics_dt消耗剩下的时间

        print('开始校时')
        # 校时并确定每个player对应的address
        while len(self.players_address) != len(self.player_names):
            print(self.players_address)
            pass
        print('完成校时')
        time.sleep(10)
        print('开始发送游戏开始时间')
        self.send_start_game_time(gf.get_time()+5)  # 等五秒之后开始游戏
        print('游戏开始时间发送成功')
        surplus_dt -= 5

        while self.is_run[0]:
            pygame.event.pump()
            delta_t = clock.tick(self.settings.max_fps) / 1000  # 获取delta_time(sec)并限制最大帧率
            now_ms = pygame.time.get_ticks()  # 测试用，当前时间
            if now_ms - printed_ms >= 2000:  # 每2秒输出一次fps等信息
                printed_ms = now_ms
                print('fps:', clock.get_fps())
                print('飞船信息:')
                for ship in self.gm.ships:
                    print('\t', ship.player_name, ':', ship.hp, ship.loc, ship.spd.length())
                print('子弹总数:', len(self.gm.bullets))

            # 在server.main更新玩家操作状态

            surplus_dt += delta_t
            while surplus_dt >= physics_dt:
                surplus_dt -= physics_dt
                # gf.check_collisions(gm)
                self.gm.all_move(physics_dt)
                # gf.ships_fire_bullet(settings, gm)

            # 向房间所有玩家广播当前gm最新状态
            self.send_gm_msg()

            gf.add_traces(self.settings, self.gm, traces, now_ms)

            surplus_ratio = surplus_dt / physics_dt
            gf.update_screen(self.settings, self.gm, camera, traces, surplus_ratio)

    def send_all(self, msg: dict):
        """向所有玩家广播msg"""
        for address in self.players_address.values():
            self.net.send(address, msg)

    def send_start_game_time(self, start_time):
        """向所有玩家广播游戏开始时间"""
        msg = {
            'type': MsgType.ServerStartGameTime,
            'time': start_time,
            'args': [self.id],
            'kwargs': {}
        }
        self.send_all(msg)

    def send_gm_msg(self):
        """向房间所有玩家广播当前gm最新状态"""
        msg = {
            'type': MsgType.AllObjs,
            'time': gf.get_time(),
            'args': [self.gm.make_planets_msg(),
                     [self.gm.make_ships_msg(), self.gm.make_dead_players_name_msg()],
                     self.gm.make_bullets_msg()],
            'kwargs': {}
        }
        self.send_all(msg)

    def load_ctrl_msg(self, player_name, ctrl_msg):
        """加载操作信息"""
        ship = gf.find_player_ship(self.gm.ships, player_name)
        ship.load_ctrl_msg(ctrl_msg)

    def send_check_clock_msg(self, player_name, addr):
        """对玩家发送校时消息"""
        self.players_address[player_name] = addr

        msg = {
            'type': MsgType.CheckClock,
            'time': gf.get_time(),
            'args': [self.id, player_name],
            'kwargs': {}
        }
        self.net.send(self.players_address[player_name], msg)
