from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.local_game_scene import LocalGameScene
import pygame


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        labels = []
        boxes = []
        menu_online_rect = pygame.Rect(455, 360, 290, 80)
        menu_online_button = Button('online game', self.online_is_clicked, menu_online_rect,
                                    self.settings.btbg_light, 0, '线上房间', SceneFont.menu_font)
        menu_online_button.add_img(self.settings.btbg_light_pressed)
        buttons = [self.back, menu_online_button]
        self.loaded = {'label': labels, 'box': boxes, 'button': buttons, 'panel': []}

    def show(self):
        self.screen.fill((10, 10, 10))
        pygame.draw.rect(self.screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        self.draw_elements(self.screen)
        pygame.display.flip()

    def local_is_clicked(self):
        ScenePlayer.push(LocalGameScene())  # 留给游戏登录
        pass

    def online_is_clicked(self):
        # ScenePlayer.push()
        pass
