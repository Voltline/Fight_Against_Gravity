import pygame
import sys
from content.UI.button_class import Button
from content.scene.scene_player_class import ScenePlayer


class Scene:

    screen = None
    settings = None
    client = None
    path = None

    def __init__(self):
        self.loaded = {'img': None, 'label': None, 'box': None, 'button': None, 'panel': None}
        """全局组件，返回按钮和设置按钮"""
        back_rect = pygame.Rect(20, 20, 45, 45)
        self.back = Button("back", self.back_is_clicked, back_rect, self.path + "assets\\Img\\back.png", 1)
        self.reminder_panel_rect = (200, 300, 800, 200)
        self.reminder_panel_rect_small = (450, 300, 300, 100)
        self.menu_like_panel_rect = (300, 200, 600, 400)
        # set_rect = pygame.Rect(1050, 700, 60, 60)
        # self.set_button = Button('setting', self.set_is_clicked, set_rect, "UI/Img/setting_light.png", 1)
        # self.set_button.add_img("UI/Img/setting_light_pressed.png")
        self.switcher = 0
        self.box_is_able = True

        """用于判断按下回车键时是否相应，如果是登录界面，敲下回车应该等同于登录，如果注册界面，敲下回车等同于进行注册"""
        self.id = 0  # 0对应登录，1对应注册，2对应设置改键，3对应无响应。

    def ban_inputbox(self):
        self.box_is_able = False

    def deal_event(self, e):
        """将对应页面加载了的组件全部进行状态更新，会post新的event"""
        if self.loaded['panel'] is not None:
            for pn in self.loaded['panel']:
                pn.update(e)
        if self.loaded['button'] is not None:
            for bt in self.loaded['button']:
                bt.update(e)
        if self.loaded['box'] is not None and self.box_is_able:
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.loaded['box'])):
                    if self.loaded['box'][i].boxBody.collidepoint(e.pos):  # 若按下鼠标且位置在文本框
                        self.loaded['box'][i].switch()
                        self.switcher = i
                    else:
                        self.loaded['box'][i].active = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    for m in self.loaded['box']:
                        m.active = False
                    self.switcher = (self.switcher + 1) % len(self.loaded['box'])
                    self.loaded['box'][self.switcher].active = True
            for bx in self.loaded['box']:
                bx.deal_event(e)

    def update(self):
        for event in pygame.event.get():
            ScenePlayer.STACK[-1].deal_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_elements(self, surface):
        if self.loaded['button'] is not None:
            for bt in self.loaded['button']:
                bt.render(surface)
        if self.loaded['label'] is not None:
            for lb in self.loaded['label']:
                lb.render(surface)
        if self.loaded['box'] is not None:
            for bx in self.loaded['box']:
                bx.render(surface)
        if self.loaded['panel'] is not None:
            for pn in self.loaded['panel']:
                pn.render(surface)

    def back_is_clicked(self):
        ScenePlayer.pop()

    def show(self):
        pass

    @staticmethod
    def init(settings, screen, client):
        Scene.settings = settings
        Scene.path = settings.path
        Scene.screen = screen
        Scene.client = client
