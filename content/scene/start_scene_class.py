from content.scene.local_game_scene import LocalGameScene
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.login_scene_class import LogInScene
import pygame


class StartScene(Scene):
    def __init__(self):
        """准备开始界面的组件"""
        super().__init__()
        start_font = SceneFont.start_font
        start_rect = pygame.Rect(455, 280, 290, 100)
        start_title = pygame.image.load(self.path + "assets\\texture\\FAGtitle.png")  # 用作画图
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()

        start = Button("start", self.start_is_clicked, start_rect,
                       self.path + "assets\\Img\\start_unpressed.png", 1, 'Start', start_font)  # 用作画图
        start.add_img(self.path + "assets\\Img\\start_press.png")

        local_rect = pygame.Rect(455, 450, 290, 100)
        local_button = Button('local game', self.local_is_clicked, local_rect,
                                   self.path + "assets\\Img\\start_unpressed.png", 0, '本地游戏', SceneFont.start_font)
        local_button.add_img(self.path + "assets\\Img\\start_press.png")
        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': None, 'box': None, 'button': [start, local_button, self.set_button], 'panel': []}

    def start_is_clicked(self):
        ScenePlayer.push(LogInScene())

    def local_is_clicked(self):
        ScenePlayer.push(LocalGameScene())  # 留给游戏登录
        pass

    def show(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.loaded['img'], (10, 10))
        self.draw_elements()
        pygame.display.flip()



