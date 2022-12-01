import pygame
from pygame import Vector2

from content.maps.map_obj import Map
from content.game_manager import GameManager
from content.camera import Camera
from Web.Modules.OptType import OptType
import content.game_function as gf


class OnlineGame:
    """在线游戏，作为基类使用"""
    def __init__(self, settings, net, room_id, map_name, player_names):
        self.settings = settings
        self.net = net
        self.room_id = room_id
        self.map = Map(map_name)
        self.player_names = player_names
        self.gm = GameManager(self.settings)
        self.clock = pygame.time.Clock()  # 准备时钟

        # 鼠标位置信息，每帧实时更新
        self.mouse_loc = Vector2(0, 0)
        self.mouse_d_loc = Vector2(0, 0)

        self.start_time = 0  # 开始游戏的时间(自己的时钟)
        self.delta_t = 0  # 这帧(上帧)经过的时间(秒)
        self.surplus_dt = 0  # 这帧需要运算的时间(秒)
        self.now_time = 0  # 从这轮开始到现在的时间

    def restart(self):
        """重置状态到游戏开始"""
        self.gm.load_map(self.map, self.player_names)
        self.start_time = self.get_start_time()
        self.now_time = self.surplus_dt = gf.get_time() - self.start_time

    def get_start_time(self) -> float:
        """虚函数，需要子类重载"""
        return gf.get_time()

    def main(self):
        self.restart()
        printed_sec = 0  # TODO:测试用，上次输出调试信息的时间
        physics_dt = self.settings.physics_dt


