import sys
import time

import pygame
from content.scene.scene_class import Scene
from content.scene.scene_player_class import ScenePlayer
from content.games.client_game import ClientGame
from content.UI.ui_function import UIFunction as UIF
from content.online.player_info import PlayerInfo


class ClientGameScene(Scene):
    """客户端在线游戏的场景"""
    def __init__(self, map_name, player_names):
        super().__init__()
        self.pause_panel = UIF.new_pause_panel(self)
        self.pause_panel.is_show = self.pause_panel.is_able = False
        self.loaded = {'img': None, 'label': None, 'box': None,
                       'button': [], 'panel': [self.pause_panel], 'msgbox': []}

        self.game = ClientGame(self.settings, self.client.client, self.client.roomid,
                               map_name, player_names, self.screen, PlayerInfo.player_name)
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

    def update(self):
        self.deal_events()
        self.game.main_update()
