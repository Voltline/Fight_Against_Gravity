import sys

import pygame
from Start_Scene_Class import StartScene
from Login_Scene_Class import LogInScene

class ScenePlayer:
    STACK = []
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))

    def push(self, scene):
        self.STACK.append(scene)

    def pop(self):
        self.STACK.pop()

    def show_scene(self, scene):
        self.push(scene)
        while True:
            for event in pygame.event.get():
                self.STACK[-1].update_event(event)
                if event.type == scene.START:
                    self.push(LogInScene())
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.STACK[-1].show(self.screen)

if __name__ == '__main__':
    s = ScenePlayer()
    s.show_scene(StartScene())
