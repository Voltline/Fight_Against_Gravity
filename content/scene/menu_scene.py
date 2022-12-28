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
        menu_online_rect = pygame.Rect(0.3792*self.width, 0.45*self.height, 0.242*self.width, 0.1*self.height)
        menu_online_button = Button('online game', self.online_is_clicked, menu_online_rect,
                                    self.settings.btbg_light, 0, '线上房间', SceneFont.menu_font)
        menu_online_button.add_img(self.settings.btbg_light_pressed)
        buttons = [self.back, self.set_button, menu_online_button]
        self.loaded = {'label': labels, 'box': boxes, 'button': buttons, 'panel': []}

    def show(self):
        self.screen.fill((10, 10, 10))
        pygame.draw.rect(self.screen, (46, 46, 46), (0.25*self.width, 0.25*self.height, 0.5*self.width, 0.5*self.height), border_radius=15)
        self.draw_elements()
        pygame.display.flip()

    def local_is_clicked(self):
        ScenePlayer.push(LocalGameScene())  # 留给游戏登录
        pass

    def online_is_clicked(self):
        # ScenePlayer.push()
        pass
