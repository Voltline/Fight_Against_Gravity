import pygame
import time
from online_game import OnlineGame
from content.camera import Camera
import content.game_function as gf
from Web.Modules.OptType import OptType


class ServerGame(OnlineGame):
    def __init__(self, settings, net, room_id, map_name, player_names):
        super().__init__(settings, None, net, room_id, map_name, player_names)
        self.camera = None  # TODO：调试完成后去掉screen和camera
        self.addresses = {}  # {player_name: address}

        self.sended_time = 0  # 上次广播消息的时间

    def main(self):
        """最终要调用的函数"""
        self.screen = gf.init_pygame_window(self.settings)
        self.camera = Camera(self.settings, self.screen)

        print('开始校时')
        # 校时并确定每个player对应的address
        while len(self.addresses) != len(self.player_names):
            # print(self.addresses)
            pass
        print('完成校时')

        super().main()

    def get_start_time(self) -> float:
        print('开始发送游戏开始时间')
        start_time = gf.get_time()+3
        self.send_start_game_time(start_time)
        print('游戏开始时间发送成功')
        return start_time

    def send_start_game_time(self, start_time):
        """向所有玩家广播游戏开始时间"""
        msg = {
            'opt': OptType.ServerStartGameTime,
            'time': start_time,
            'args': [self.room_id],
            'kwargs': {}
        }
        self.send_all(msg)

    def send_all(self, msg: dict):
        """向所有玩家广播msg"""
        for address in self.addresses.values():
            self.net.send(address, msg)

    def physic_update(self):
        """每个物理dt的更新行为"""
        super().physic_update()
        self.gm.check_collisions()
        self.gm.all_move(self.physics_dt)
        self.gm.ships_fire_bullet()

    def send_msgs(self):
        """发送消息"""
        # 向房间所有玩家广播当前gm最新状态
        if self.now_time - self.sended_time > self.physics_dt:
            self.send_gm_msg()
            self.sended_time = self.now_time

    def send_gm_msg(self):
        """
        向房间所有玩家广播当前gm最新状态
        分开发送，避免数据包过长
        """
        # 广播all_ships
        msg = {
            'opt': OptType.AllShips,
            'tick': self.now_tick,
            'args': [self.gm.make_ships_msg(), self.gm.make_dead_players_name_msg()]
        }
        self.send_all(msg)

        # 广播bullets
        msg = {
            'opt': OptType.Bullets,
            'tick': self.now_tick,
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
            'args': [self.room_id, player_name],
            'kwargs': {}
        }
        self.net.send(self.addresses[player_name], msg)

    def check_events(self):
        """服务器不需要处理消息"""
        # TODO：调试完成后把此函数pass
        self.mouse_loc.update(pygame.mouse.get_pos())
        self.mouse_d_loc.update(pygame.mouse.get_rel())
        self.camera.mouse_loc.update(self.mouse_loc)

        event = pygame.event.poll()
        while event:
            if event.type == pygame.QUIT:
                self.is_run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # 是否按下鼠标中键
                    self.camera.change_mode()
            elif event.type == pygame.MOUSEMOTION:
                mouse_keys = pygame.mouse.get_pressed()
                if mouse_keys[2]:  # 如果鼠标右键被按下
                    self.camera.d_loc.update(self.mouse_d_loc)
            elif event.type == pygame.MOUSEWHEEL:
                self.camera.d_zoom = event.y

            event = pygame.event.poll()

    def display(self):
        """更新屏幕"""
        # TODO：调试完成后本函数删除
        surplus_ratio = self.surplus_dt / self.physics_dt
        gf.update_screen(self.settings, self.gm, self.camera, [], surplus_ratio)
