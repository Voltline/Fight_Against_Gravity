import sys
import pygame
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.UI.panel_class import Panel
from content.game.local_game import LocalGame


class LocalGameScene(Scene):
    def __init__(self):
        super().__init__()
        pause_rect = pygame.Rect(1060, 750, 30, 30)
        """暂停按钮"""
        pause_button = Button('pause', self.pause_is_clicked, pause_rect, self.path + 'assets\\Img\\pause.png', 0)
        pause_button.add_img(self.path + 'assets\\Img\\pause_pressed.png')
        """暂停后panel上的组件"""

        """返回主界面"""
        go_menu_rect = pygame.Rect(0, 0, 300, 65)
        go_menu_button = Button('go menu', self.go_menu_is_clicked, go_menu_rect,
                                self.settings.btbg_light, 0, '返回主界面', SceneFont.log_font)
        go_menu_button.add_img(self.settings.btbg_light_pressed)
        """退出游戏"""
        exit_rect = pygame.Rect(0, 0, 300, 65)
        exit_button = Button('exit', self.exit_is_clicked, exit_rect,
                             self.settings.btbg_light, 0, '退出游戏', SceneFont.log_font)
        exit_button.add_img(self.settings.btbg_light_pressed)
        pause_panel_components_relative_pos = {'button': [[0.88, 0.1], [0.25, 0.15], [0.25, 0.4]],
                                               'box': [[]]}
        self.pause_panel = Panel(self.menu_like_panel_rect, '已暂停', 23,
                                 [self.close_button, go_menu_button, exit_button], [], pause_panel_components_relative_pos, text_pos=0, has_scrollbar=True)
        print("after pause_panel is created, its loaded['button'] has", len(self.pause_panel.loaded['button']))
        self.loaded = {'img': None, 'label': None, 'box': None,
                       'button': [], 'panel': []}

        self.game = LocalGame(self.settings, self.screen, '地月系统')
        self.game.restart()

    def pause_is_clicked(self):
        self.loaded['panel'] = [self.pause_panel]
        self.game.is_pause = True

    def close_is_clicked(self):
        self.loaded['panel'] = []
        self.game.is_pause = False

    def go_menu_is_clicked(self):
        ScenePlayer.pop()

    def exit_is_clicked(self):
        pygame.quit()
        sys.exit()

    def show(self):
        self.draw_elements()
        pygame.display.flip()

    def deal_event(self, e):
        super().deal_event(e)
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            if self.game.is_pause:
                self.close_is_clicked()
            else:
                self.pause_is_clicked()

    def deal_events(self):
        """获取并处理所有消息"""
        self.game.mouse_loc.update(pygame.mouse.get_pos())
        self.game.mouse_d_loc.update(pygame.mouse.get_rel())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                ScenePlayer.STACK[-1].deal_event(event)
                if not self.game.is_pause:
                    self.game.deal_event(event)

    def update(self):
        self.deal_events()
        self.game.main_update()
