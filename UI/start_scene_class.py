import sys
from scene_class import Scene
from button_class import Button
from scene_events import SceneEvents
from scene_settings import SceneSetting
from scene_font import SceneFont
from scene_player_class import ScenePlayer
from login_scene_class import LogInScene
import os
import pygame


class StartScene(Scene):
    def __init__(self, setting):
        """准备开始界面的组件, 对应页面状态 0"""
        super().__init__(setting)
        os.chdir(self.setting.fag_directory)  # 文件路径老是出错
        start_font = SceneFont.start_font
        start_rect = pygame.Rect(455, 300, 290, 100)
        start_title = pygame.image.load("assets/texture/FAGtitle.png")  # 用作画图
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()

        start = Button("start", self.start_is_clicked, start_rect, "UI/Img/start_unpressed.png", 1, 'Start', start_font)  # 用作画图
        start.add_img("UI/Img/start_press.png")
        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': None, 'box': None, 'button': [start], 'panel': None}

    def start_is_clicked(self):
        ScenePlayer.push(LogInScene(self.setting))



    def show(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.loaded['img'], (10, 10))
        self.draw_elements(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    running = True
    screen = pygame.display.set_mode((1200, 800))
    setting_ = SceneSetting()
    m = StartScene(setting_)
    while running:
        for event in pygame.event.get():
            m.update_event(event)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        m.show(screen)
