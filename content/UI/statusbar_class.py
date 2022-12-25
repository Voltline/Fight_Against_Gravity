import pygame
import os
import sys
from content.scene.scene_font import SceneFont
from content.UI.label_class import Label
from content.UI.hp import HP
from content.UI.panel_class import Panel


class StatusBar:
    def __init__(self, settings, username: str):
        self.font = pygame.font.Font(settings.path + "assets\\font\\SourceHanSans-Normal.ttc", 16)

        self.name_label = Label(0, 0, 60, username, SceneFont.nickname_font)
        self.hp_bar = HP(0, 0, settings)
        self.hp_bar.r_xy = 0, 0.5
        self.hp_value_label = Label(0, 0, 60, str(self.hp_bar.hp), SceneFont.hp_value_font)
        self.hp_value_label.rect.height = 10
        self.hp_value_label.r_xy = 0, 0.5
        self.hp_panel = Panel(pygame.Rect(0, 0, 60, 30), '', 20,
                              others=[self.name_label, self.hp_bar, self.hp_value_label])
        self.hp_panel.color = (1, 1, 1)  # panel背景设成透明

    def render(self, screen):
        self.hp_panel.render(screen)

    def update_hp(self, new_hp):
        self.hp_bar.update_hp(new_hp)
        self.hp_value_label.set_text(str(new_hp)+'/'+str(self.hp_bar.full_hp))

    def set_left_top(self, left, top):
        """设置hp_panel的rect的left和top"""
        self.hp_panel.rect.left = left
        self.hp_panel.rect.top = top
