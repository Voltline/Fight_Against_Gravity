import pygame
import os
import sys
from inputbox_class import InputBox
from button_class import Button
from label_class import Label
from start_scene_class import StartScene
from login_scene_class import LogInScene
from register_scene_class import RegScene
from scene_settings import SceneSetting
from scene_font import SceneFont
from scene_player_class import ScenePlayer


if __name__ == "__main__":
    pygame.init()
    print(os.getcwd())
    sc = pygame.display.set_mode((1200, 800))
    setting = SceneSetting()
    begin = StartScene(setting)
    sp = ScenePlayer(sc, setting)
    ScenePlayer.push(begin)
    sp.show_scene()
