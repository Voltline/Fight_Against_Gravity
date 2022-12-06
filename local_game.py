import pygame

from fag_game import FAGGame
import content.game_function as gf
from content.camera import Camera


class LocalGame(FAGGame):
    """本地游戏"""
    def __init__(self, settings, screen, map_name, time_scale=1):
        super().__init__(settings, screen, map_name, ['player1', 'player2'], time_scale)
        self.ship1 = None
        self.ship2 = None
        self.camera = Camera(settings, screen)
        self.traces = []

    def restart(self):
        """重置状态到游戏开始"""
        super().restart()
        self.ship1 = gf.find_player_ship(self.gm.ships, 'player1')
        self.ship2 = gf.find_player_ship(self.gm.ships, 'player2')
        self.traces = []

    def events_loop(self):
        """更新消息的循环"""
        self.camera.mouse_loc.update(self.mouse_loc)
        super().events_loop()

    def deal_event(self, event):
        super().deal_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # 是否按下鼠标中键
                self.camera.change_mode()
        elif event.type == pygame.MOUSEMOTION:
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[2]:  # 如果鼠标右键被按下
                self.camera.d_loc.update(self.mouse_d_loc)
        elif event.type == pygame.MOUSEWHEEL:
            self.camera.d_zoom = event.y

        elif event.type == pygame.KEYDOWN:
            self.check_events_keydown(event)
        elif event.type == pygame.KEYUP:
            self.check_events_keyup(event)

    def check_events_keydown(self, event):
        """处理按下按键"""
        if event.key == self.settings.ship1_k_go_ahead:
            self.ship1.is_go_ahead = True
        elif event.key == self.settings.ship1_k_go_back:
            self.ship1.is_go_back = True
        elif event.key == self.settings.ship1_k_turn_left:
            self.ship1.is_turn_left = True
        elif event.key == self.settings.ship1_k_turn_right:
            self.ship1.is_turn_right = True
        elif event.key == self.settings.ship1_k_fire:
            self.ship1.is_fire = True

        elif event.key == self.settings.ship2_k_go_ahead:
            self.ship2.is_go_ahead = True
        elif event.key == self.settings.ship2_k_go_back:
            self.ship2.is_go_back = True
        elif event.key == self.settings.ship2_k_turn_left:
            self.ship2.is_turn_left = True
        elif event.key == self.settings.ship2_k_turn_right:
            self.ship2.is_turn_right = True
        elif event.key == self.settings.ship2_k_fire:
            self.ship2.is_fire = True

    def check_events_keyup(self, event):
        """处理松开按键"""
        if event.key == self.settings.ship1_k_go_ahead:
            self.ship1.is_go_ahead = False
        elif event.key == self.settings.ship1_k_go_back:
            self.ship1.is_go_back = False
        elif event.key == self.settings.ship1_k_turn_left:
            self.ship1.is_turn_left = False
        elif event.key == self.settings.ship1_k_turn_right:
            self.ship1.is_turn_right = False
        elif event.key == self.settings.ship1_k_fire:
            self.ship1.is_fire = False

        elif event.key == self.settings.ship2_k_go_ahead:
            self.ship2.is_go_ahead = False
        elif event.key == self.settings.ship2_k_go_back:
            self.ship2.is_go_back = False
        elif event.key == self.settings.ship2_k_turn_left:
            self.ship2.is_turn_left = False
        elif event.key == self.settings.ship2_k_turn_right:
            self.ship2.is_turn_right = False
        elif event.key == self.settings.ship2_k_fire:
            self.ship2.is_fire = False

    def physic_update(self):
        """每个物理dt的更新行为"""
        super().physic_update()
        self.gm.check_collisions()
        self.gm.all_move(self.physics_dt)
        self.gm.ships_fire_bullet()

    def physic_loop(self):
        """在基类的物理循环之后要删除子弹，添加尾迹"""
        super().physic_loop()
        self.gm.bullets_disappear()
        gf.add_traces(self.settings, self.gm, self.traces, self.now_time)

    def display(self):
        """更新屏幕"""
        surplus_ratio = self.surplus_dt / self.physics_dt
        gf.update_screen(self.settings, self.gm, self.camera, self.traces, surplus_ratio, self.now_time)
