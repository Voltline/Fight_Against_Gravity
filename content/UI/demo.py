import pygame
import os
import sys
from content.UI.inputbox_class import InputBox
from content.UI.button_class import Button
from content.UI.label_class import Label
from content.UI.start_scene_class import StartScene
from content.UI.login_scene_class import LogInScene
from content.UI.register_scene_class import RegScene
from content.UI.scene_settings import SceneSetting
from content.UI.scene_font import SceneFont
from content.UI.scene_player_class import ScenePlayer


if __name__ == "__main__":
    pygame.init()
    print(os.getcwd())
    sc = pygame.display.set_mode((1200, 800))
    setting = SceneSetting()
    begin = StartScene(setting)
    sp = ScenePlayer(sc, setting)
    ScenePlayer.push(begin)
    sp.show_scene()
