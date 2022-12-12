import pygame

from content.UI.scene_class import Scene
from content.UI.label_class import Label
from content.UI.scene_player_class import ScenePlayer


class NoCheckErr(Scene):
    def __init__(self, setting):
        super().__init__(setting)
        self.reminder = Label(500, 550, 150, "未输入验证码!")
        self.loaded = None

    def draw_reminder(self, screen):
        self.reminder.render(screen)

    def deal_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            ScenePlayer.pop()
