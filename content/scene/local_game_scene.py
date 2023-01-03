import sys
import pygame
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.UI.panel_class import Panel
from content.games.local_game import LocalGame
from content.UI.ui_function import UIFunction as UIF


class LocalGameScene(Scene):
    """本地游戏的场景"""
    def __init__(self, map_name):
        super().__init__()
        self.pause_panel = UIF.new_pause_panel(self)
        self.pause_panel.is_show = self.pause_panel.is_able = False
        self.win_panel = UIF.new_local_game_win_panel(self, '本局无人生还')
        self.win_panel.is_show = self.win_panel.is_able = False
        self.loaded = {'img': None, 'label': None, 'box': None,
                       'button': [], 'panel': [self.pause_panel, self.set_panel, self.win_panel], 'msgbox': []}

        self.game = LocalGame(self.settings, self.screen, map_name)
        self.game.restart()

    def pause_clicked(self):
        if not self.set_panel.is_show and not self.win_panel.is_show:
            self.pause_panel.is_show = self.pause_panel.is_able = True
            self.game.is_pause = True

    def continue_button_clicked(self):
        if not self.set_panel.is_show:
            self.pause_panel.is_show = self.pause_panel.is_able = False
            self.game.is_pause = False

    def show(self):
        self.draw_elements()
        pygame.display.flip()

    def deal_event(self, e):
        super().deal_event(e)
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            if self.set_panel.is_show:
                self.set_key_clicked()
            elif self.game.is_pause:
                self.continue_button_clicked()
            else:
                self.pause_clicked()

    def deal_events(self):
        """获取并处理所有消息"""
        self.game.mouse_loc.update(pygame.mouse.get_pos())
        self.game.mouse_d_loc.update(pygame.mouse.get_rel())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.deal_event(event)
                if not self.game.is_pause:
                    self.game.deal_event(event)

    def check_win(self):
        """判断游戏是否胜利"""
        if self.game.is_run and len(self.game.gm.ships) < 2:
            if len(self.game.gm.ships) == 1:  # 有一个人活着
                self.win_panel.loaded['others'][1].set_text(
                    self.game.gm.ships.sprites()[0].player_name)
            else:  # 无人生还
                self.win_panel.loaded['others'][1].set_text('本局无人生还')
            self.win_panel.is_show = self.win_panel.is_able = True
            self.game.is_run = False

    def win_panel_continue_button_clicked(self):
        """点击了win_panel上的继续按钮"""
        self.win_panel.is_show = self.win_panel.is_able = False

    def win_panel_restart_button_clicked(self):
        """点击了win_panel上的重新开始按钮"""
        self.win_panel.is_show = self.win_panel.is_able = False
        self.game.is_run = True
        self.game.restart()

    def update(self):
        self.deal_events()
        self.game.main_update()
        self.check_win()

