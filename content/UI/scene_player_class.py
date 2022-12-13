import os
import sys
import pygame
from content.UI.scene_settings import SceneSetting


class ScenePlayer:
    STACK = []

    @staticmethod
    def push(scene):
        ScenePlayer.STACK.append(scene)

    @staticmethod
    def pop():
        ScenePlayer.STACK.pop()

    def __init__(self, screen, setting):
        self.screen = screen
        self.check_code = ''
        self.setting = setting

    def show_scene(self):
        while True:
            for event in pygame.event.get():
                ScenePlayer.STACK[-1].update_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            ScenePlayer.STACK[-1].show(self.screen)


if __name__ == '__main__':
    pygame.init()
    scene_setting = SceneSetting()
    print(os.getcwd())
    sc = pygame.display.set_mode((1200, 800))
    s = ScenePlayer(sc, scene_setting)
    s.show_scene()
