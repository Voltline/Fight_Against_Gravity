import pygame
from pygame import Vector2
import sys
from content.maps.map_obj import Map
from content.space_objs.game_manager import GameManager
import content.game_modules.game_function as gf


class FAGGame:
    """一局游戏，作为基类使用"""
    def __init__(self, settings, screen, map_name, player_names, time_scale=1):
        self.settings = settings
        self.screen = screen
        self.map = Map(map_name)
        self.player_names = player_names
        self.gm = GameManager(self.settings)
        self.clock = pygame.time.Clock()  # 准备时钟
        self.time_scale = time_scale

        # 鼠标位置信息，每帧实时更新
        self.mouse_loc = Vector2(0, 0)
        self.mouse_d_loc = Vector2(0, 0)

        # 时间相关
        self.max_fps = self.settings.max_fps
        self.start_time = 0  # 开始游戏的时间(自己的时钟)
        self.delta_t = 0  # 这帧(上帧)经过的时间(秒)
        self.surplus_dt = 0  # 这帧需要运算的时间(秒)
        self.now_time = 0  # 从这轮开始到现在的时间
        self.now_tick = 0  # 从这轮开始到现在经过的物理tick数
        self.physics_dt = self.settings.physics_dt

        self.is_run = True  # 是否仍在运行
        self.is_pause = False  # 是否处于暂停状态

    def restart(self):
        """重置状态到游戏开始"""
        self.gm.load_map(self.map, self.player_names)
        self.start_time = self.get_start_time()
        self.surplus_dt = gf.get_time() - self.start_time
        self.clock.tick(self.max_fps)
        self.now_time = 0
        self.now_tick = 0

    def get_start_time(self) -> float:
        """获取游戏开始的本地时间"""
        return gf.get_time()

    def main(self):
        """程序入口"""
        self.restart()
        self.main_loop()
        self.end()

    def main_loop(self):
        """主循环"""
        printed_time = 0  # TODO:测试用，上次输出调试信息的时间
        while self.is_run:
            if self.now_time - printed_time > 1:  # 每1秒输出一次fps等信息
                printed_time = self.now_time
                self.print_debug()
            self.main_update()

    def main_update(self):
        """主循环每轮要做的事情"""
        # if not self.is_pause:  # 不暂停才处理pygame的events
        #     self.check_events()
        self.delta_t = self.time_scale*self.clock.tick(self.max_fps)/1000  # 获取delta_time(sec)并限制最大帧率
        self.surplus_dt += self.delta_t
        self.physic_loop()
        self.display()

    def print_debug(self):
        """输出调试的信息"""
        if "--nogui" not in sys.argv:
            print('now:', self.now_time, '; tick:', self.now_tick)
            print('fps:', 1/self.delta_t)
            print('飞船信息:')
            for ship in self.gm.ships:
                print('\t', ship.player_name, ':', ship.hp, ship.loc, ship.spd.length(), ship.make_ctrl_msg())
            print('子弹总数:', len(self.gm.bullets))
            print()

    def end(self):
        """主循环结束之后要做的事情"""
        pass

    def check_events(self):
        """响应键盘和鼠标事件，需要重载"""
        self.mouse_loc.update(pygame.mouse.get_pos())
        self.mouse_d_loc.update(pygame.mouse.get_rel())
        self.events_loop()

    def events_loop(self):
        """更新消息的循环"""
        event = pygame.event.poll()
        while event:
            self.deal_event(event)
            event = pygame.event.poll()

    def deal_event(self, event):
        """处理消息"""
        if event.type == pygame.QUIT:
            self.is_run = False

    def display(self):
        """更新屏幕"""
        pass

    def physic_loop(self):
        """物理dt更新的循环"""
        while self.surplus_dt >= self.physics_dt:
            self.physic_update()
            self.bullets_disappear()

    def physic_update(self):
        """每个物理dt的更新行为"""
        self.surplus_dt -= self.physics_dt
        self.now_time += self.physics_dt
        self.now_tick += 1

    def bullets_disappear(self) -> list:
        """让太远离战场的子弹消失, 返回消失的子弹的id的列表"""
        return self.gm.bullets_disappear()
