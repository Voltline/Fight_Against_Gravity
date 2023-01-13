import sys
import time

import pygame
from content.scene.scene_class import Scene
from content.scene.scene_player_class import ScenePlayer
from content.games.client_game import ClientGame
from content.UI.ui_function import UIFunction as UIF
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.online.player_info import PlayerInfo


class ClientGameScene(Scene):
    """客户端在线游戏的场景"""

    def __init__(self, map_name, player_names, server_start_time=None):
        super().__init__()
        self.pause_panel = UIF.new_pause_panel(self)
        self.pause_panel.is_show = self.pause_panel.is_able = False
        self.win_panel, self.return_room_button, self.win_panel_label = UIF.new_client_game_win_panel(self, '')
        self.win_panel.is_show = self.win_panel.is_able = False
        self.player_ship_far_label = UIF.new_client_game_scene_far_label(self)
        self.player_ship_far_label.is_show = False
        self.loaded = {'img': None, 'label': [self.player_ship_far_label], 'box': None,
                       'button': [], 'panel': [self.pause_panel, self.win_panel], 'msgbox': []}
        self.bgm_id = 2

        self.return_room_countdown_time = 5
        self.game = ClientGame(self.settings, self.client.client, self.client.client, self.client.roomid,
                               map_name, player_names, self.screen, PlayerInfo.player_name,
                               server_start_time)
        self.last_ping_ms = 0
        self.display_ping_ms = 0
        self.ping_label = Label(0.97 * self.screen.get_rect().width, 0.02 * self.screen.get_rect().height,
                                10, f"{int(self.game.ping_ms)} ms", SceneFont.ping_good_font)
        self.ping_time = time.time()
        self.loaded['label'].append(self.ping_label)
        self.game.restart()

    def pause_clicked(self):
        self.pause_panel.is_show = self.pause_panel.is_able = True
        self.game.is_pause = True

    def continue_button_clicked(self):
        self.pause_panel.is_show = self.pause_panel.is_able = False
        self.game.is_pause = False

    def quit_button_clicked(self):
        ClientGameScene.client.leftroom()
        time.sleep(1)
        self.client.client.get_message_list()

        ScenePlayer.pop()
        ScenePlayer.pop()

    def return_room_button_clicked(self):
        """点击胜利panel上的返回房间按钮"""
        ScenePlayer.pop()

    def show(self):
        self.draw_elements()
        pygame.display.flip()

    def deal_event(self, e) -> bool:
        if super().deal_event(e):
            return True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            if self.set_panel.is_show:
                self.set_key_clicked()
            elif self.game.is_pause:
                self.continue_button_clicked()
            else:
                self.pause_clicked()
        return False

    def deal_events(self):
        """获取并处理所有消息"""
        self.game.mouse_loc.update(pygame.mouse.get_pos())
        self.game.mouse_d_loc.update(pygame.mouse.get_rel())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if self.deal_event(event):
                    continue
                if not self.game.is_pause:
                    self.game.deal_event(event)

    def check_win(self):
        """判断游戏是否胜利"""
        if self.game.is_run and self.game.win_player is not None:
            self.game.is_run = False
            self.win_panel_label.set_text(self.game.win_player)
            self.win_panel.is_show = self.win_panel.is_able = True

    def return_room_countdown(self):
        """返回房间5秒倒计时，倒计时结束自动按按钮"""
        if self.win_panel.is_show:
            self.return_room_countdown_time -= self.game.delta_t
            if self.return_room_countdown_time <= 0:
                self.return_room_button_clicked()
            self.return_room_button.set_text('返回房间(' + str(int(self.return_room_countdown_time)) + ')')

    def ping_label_update(self):
        if time.time() - self.ping_time >= 1:
            self.last_ping_ms = int(self.ping_label.text.split(" ms")[0])
            self.display_ping_ms = int(0.2 * self.last_ping_ms + 0.8 * self.game.ping_ms)
            if self.display_ping_ms <= 120:
                tc = (18, 230, 53)
            elif self.display_ping_ms <= 240:
                tc = (224, 135, 33)
            else:
                tc = (209, 27, 27)
            self.ping_label.set_text(f"{self.display_ping_ms} ms", tc)
            self.ping_time = time.time()

    def update(self):
        self.deal_events()
        self.game.main_update()
        self.check_win()
        self.return_room_countdown()
        self.player_ship_far_label.is_show = self.game.player_ship_is_far
        self.ping_label_update()
