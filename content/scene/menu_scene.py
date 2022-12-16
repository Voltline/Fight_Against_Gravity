from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.local_game_scene import LocalGameScene
import pygame


class MenuScene(Scene):
    def __init__(self, setting, client_):
        super().__init__(setting, client_)
        labels = None
        boxes = None

        menu_local_rect = pygame.Rect(455, 200, 290, 80)
        menu_local_button = Button('local game', self.local_is_clicked, menu_local_rect,
                                   self.setting.btbg_light, 0, '本地游戏', SceneFont.menu_font)
        menu_online_rect = pygame.Rect(455, 360, 290, 80)
        menu_online_button = Button('online game', self.online_is_clicked, menu_online_rect,
                                    self.setting.btbg_light, 0, '线上房间', SceneFont.menu_font)
        menu_local_button.add_img(self.setting.btbg_light_pressed)
        menu_online_button.add_img(self.setting.btbg_light_pressed)
        buttons = [self.back, menu_local_button, menu_online_button]
        self.loaded = {'label': labels, 'box': boxes, 'button': buttons, 'panel': []}

    def show(self, screen):
        screen.fill((10, 10, 10))
        pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        self.draw_elements(screen)
        pygame.display.flip()

    def local_is_clicked(self):
        ScenePlayer.push(LocalGameScene(self.setting, self.client))  # 留给游戏登录
        pass

    def online_is_clicked(self):
        # ScenePlayer.push()
        pass
