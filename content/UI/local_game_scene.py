from content.UI.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.UI.scene_font import SceneFont
from content.UI.scene_player_class import ScenePlayer
from content.UI.panel_class import Panel
from Server import identify_client as ic
import os
import sys
import pygame


class LocalGameScene(Scene):
    def __init__(self, setting):
        super().__init__(setting)
        self.pause_panel = Panel(self.reminder_panel_rect, '单击此处继续', 23, self.cancel_pause_clicked)
        pause_rect = pygame.Rect(950, 675, 30, 30)
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\"
        pause_button = Button('pause', self.pause_is_clicked, pause_rect, path + 'assets\\Img\\pause.png', 0)
        pause_button.add_img(path + 'assets\\Img\\pause_pressed.png')
        self.loaded = {'img': None, 'label': None, 'box': None, 'button': [pause_button], 'panel': []}

    def pause_is_clicked(self):
        self.loaded['panel'] = [self.pause_panel]

    def cancel_pause_clicked(self):
        self.loaded['panel'] = []

    def show(self, screen):
        screen.fill((10, 10, 10))
        self.draw_elements(screen)
        pygame.display.flip()
