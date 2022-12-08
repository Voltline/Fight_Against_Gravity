import sys
from Scene_Events import SceneEvents
import pygame
from Start_Scene_Class import StartScene
from Login_Scene_Class import LogInScene
from Scene_Settings import SceneSetting


class ScenePlayer:
    def __init__(self, screen):
        self.stack = []
        self.screen = screen

    def push(self, scene):
        self.stack.append(scene)

    def pop(self):
        self.stack.pop()

    def show_scene(self, scene):
        self.push(scene)
        while True:
            for event in pygame.event.get():
                self.stack[-1].update_event(event)
                if event.type == SceneEvents.START:
                    self.push(LogInScene())
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.stack[-1].show(self.screen)


if __name__ == '__main__':
    pygame.init()
    scene_setting = SceneSetting
    sc = pygame.display.set_mode((1200, 800))
    s = ScenePlayer(sc)
    s.show_scene(StartScene())

