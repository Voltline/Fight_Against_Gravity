import sys
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_settings import SceneSetting
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.login_scene_class import LogInScene
import pygame


class StartScene(Scene):
    def __init__(self, setting):
        """准备开始界面的组件, 对应页面状态 0"""
        super().__init__(setting)
        start_font = SceneFont.start_font
        start_rect = pygame.Rect(455, 300, 290, 100)
        start_title = pygame.image.load(setting.fag_directory + "assets\\texture\\FAGtitle.png")  # 用作画图
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()

        start = Button("start", self.start_is_clicked, start_rect,
                       setting.fag_directory + "assets\\Img\\start_unpressed.png", 1, 'Start', start_font)  # 用作画图
        start.add_img(setting.fag_directory + "assets\\Img\\start_press.png")
        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': None, 'box': None, 'button': [start], 'panel': []}

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
