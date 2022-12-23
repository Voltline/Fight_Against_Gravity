import pygame
import os
import sys
from content.scene.scene_font import SceneFont
from content.UI.label_class import Label
from content.UI.hp import HP
from settings.all_settings import Settings


class StatusBar:
    def __init__(self, username: str):
        self.x = 0
        self.y = 0
        self.username = username
        # self.rect = pygame.Rect(0, 0, 90, 30)
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'
        self.font = pygame.font.Font(path + "assets\\font\\SourceHanSans-Normal.ttc", 16)

        self.Nickname = Label(self.x, self.y, 90, username, SceneFont.nickname_font)
        self.HP_bar = HP(self.x, self.y + 20, path)

    def render(self, screen):
        self.HP_bar.render(screen)
        self.Nickname.render(screen)

    def update(self, new_hp):
        self.HP_bar.update_hp(new_hp)
