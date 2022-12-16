import pygame
import os
from content.scene.start_scene_class import StartScene
from content.scene.scene_settings import SceneSetting
from content.scene.scene_player_class import ScenePlayer


if __name__ == "__main__":
    pygame.init()
    print(os.getcwd())
    sc = pygame.display.set_mode((1200, 800))
    setting = SceneSetting()
    begin = StartScene(setting)
    sp = ScenePlayer(sc, setting)
    ScenePlayer.push(begin)
    sp.show_scene()
