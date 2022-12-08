import sys
from Scene_Class import Scene
from Button_Class import Button
from Scene_Events import SceneEvents
from UI_Font import UIFont
import os
import pygame


class StartScene(Scene):
    def __init__(self, setting):
        """准备开始界面的组件, 对应页面状态 0"""
        super().__init__(setting)
        os.chdir(self.fag_directory)
        start_font = UIFont.start_font
        start_rect = pygame.Rect(455, 300, 290, 100)
        start_title = pygame.image.load("assets/texture/FAGtitle.png")  # 用作画图
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()

        start = Button("start", SceneEvents.START, start_rect, "UI/Img/start_unpressed.png", 1, 'Start', start_font)  # 用作画图
        start.add_img("UI/Img/start_press.png")
        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': None, 'box': None, 'button': [start]}

    # def handle_event(self):
    #     for event_ in pygame.event.get():
    #         self.update_event(event_)
    #         if event_.type == self.START:
    #         if event_.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         self.screen.blit(self.loaded['img'], (10, 10))
    #         self.draw_elements(self.screen)
    #         pygame.display.flip()
    def show(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.loaded['img'], (10, 10))
        self.draw_elements(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    running = True
    screen = pygame.display.set_mode((1200, 800))
    m = StartScene()
    while running:
        for event in pygame.event.get():
            m.update_event(event)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        m.show(screen)
