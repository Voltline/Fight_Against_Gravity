from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.UI.panel_class import Panel
import os
import sys
import pygame


class LocalGameScene(Scene):
    def __init__(self, setting):
        super().__init__(setting)
        pause_rect = pygame.Rect(950, 675, 20, 20)
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\"
        """暂停按钮"""
        pause_button = Button('pause', self.pause_is_clicked, pause_rect, path + 'assets\\Img\\pause.png', 0)
        pause_button.add_img(path + 'assets\\Img\\pause_pressed.png')
        """暂停后panel上的组件"""
        close_rect = pygame.Rect(0, 0, 20, 20)
        close_button = Button('close', self.close_is_clicked, close_rect, path + 'assets\\Img\\close_unclicked.png', 0)
        close_button.add_img(path + 'assets\\Img\\close_clicked.png')

        """返回主界面"""
        go_menu_rect = pygame.Rect(0, 0, 300, 65)
        go_menu_button = Button('go menu', self.go_menu_is_clicked, go_menu_rect,
                                self.setting.btbg_light, 0, '返回主界面', SceneFont.log_font)
        go_menu_button.add_img(self.setting.btbg_light_pressed)
        """退出游戏"""
        exit_rect = pygame.Rect(0, 0, 300, 65)
        exit_button = Button('exit', self.exit_is_clicked, exit_rect,
                             self.setting.btbg_light, 0, '退出游戏', SceneFont.log_font)
        exit_button.add_img(self.setting.btbg_light_pressed)
        pause_panel_components_relative_pos = {'button': [[0.88, 0.1], [0.25, 0.15], [0.25, 0.4]],
                                               'box': [[]]}
        self.pause_panel = Panel(self.menu_like_panel_rect, '已暂停', 23,
                                 [close_button, go_menu_button, exit_button], [], pause_panel_components_relative_pos, text_pos=0)
        print("after pause_panel is created, its loaded['button'] has", len(self.pause_panel.loaded['button']))
        self.loaded = {'img': None, 'label': None, 'box': None,
                       'button': [pause_button], 'panel': []}

    def pause_is_clicked(self):
        self.loaded['panel'] = [self.pause_panel]

    def close_is_clicked(self):
        self.loaded['panel'] = []

    def go_menu_is_clicked(self):
        ScenePlayer.pop()

    def exit_is_clicked(self):
        pygame.quit()
        sys.exit()

    def show(self, screen):
        screen.fill((10, 10, 10))
        self.draw_elements(screen)
        pygame.display.flip()
