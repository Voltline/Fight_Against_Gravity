from content.scene.local_game_scene import LocalGameScene
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.login_scene_class import LogInScene
import pygame


class StartScene(Scene):
    def __init__(self, setting, client_):
        """准备开始界面的组件"""
        super().__init__(setting, client_)
        start_font = SceneFont.start_font
        start_rect = pygame.Rect(455, 280, 290, 100)
        start_title = pygame.image.load(setting.fag_directory + "assets\\texture\\FAGtitle.png")  # 用作画图
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()

        start = Button("start", self.start_is_clicked, start_rect,
                       setting.fag_directory + "assets\\Img\\start_unpressed.png", 1, 'Start', start_font)  # 用作画图
        start.add_img(setting.fag_directory + "assets\\Img\\start_press.png")

        local_rect = pygame.Rect(455, 450, 290, 100)
        local_button = Button('local game', self.local_is_clicked, local_rect,
                                   setting.fag_directory + "assets\\Img\\start_unpressed.png", 0, '本地游戏', SceneFont.start_font)
        local_button.add_img(setting.fag_directory + "assets\\Img\\start_press.png")
        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': None, 'box': None, 'button': [start, local_button], 'panel': []}

    def start_is_clicked(self):
        ScenePlayer.push(LogInScene(self.setting, self.client))

    def local_is_clicked(self):
        ScenePlayer.push(LocalGameScene(self.setting, self.client))  # 留给游戏登录
        pass

    def show(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.loaded['img'], (10, 10))
        self.draw_elements(screen)
        pygame.display.flip()

    def update(self, e):
        self.deal_event(e)


