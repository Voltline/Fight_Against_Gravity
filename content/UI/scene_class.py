import pygame
from content.UI.button_class import Button
from content.UI.scene_player_class import ScenePlayer


class Scene:

    def __init__(self, setting):
        self.setting = setting  # 记得把子类所有的涉及到setting里的东西更换掉
        self.loaded = {'img': None, 'label': None, 'box': None, 'button': None, 'panel': None}
        """全局组件，返回按钮和设置按钮"""
        back_rect = pygame.Rect(20, 20, 45, 45)
        self.back = Button("back", self.back_is_clicked, back_rect, setting.fag_directory + "assets\\Img\\back.png", 1)
        self.reminder_panel_rect = (200, 300, 800, 200)
        self.reminder_panel_rect_small = (450, 300, 300, 100)
        # set_rect = pygame.Rect(1050, 700, 60, 60)
        # self.set_button = Button('setting', SceneEvents.SETTING, set_rect, "UI/Img/setting_light.png", 1)
        # self.set_button.add_img("UI/Img/setting_light_pressed.png")
        self.switcher = 0
        self.box_is_able = True

    def ban_inputbox(self):
        self.box_is_able = False
    def update_event(self, e):
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

    def draw_elements(self, surface):
        if self.loaded['button'] is not None:
            for bt in self.loaded['button']:
                bt.render(surface)
        if self.loaded['label'] is not None:
            for lb in self.loaded['label']:
                lb.render(surface)
        if self.loaded['box'] is not None:
            for bx in self.loaded['box']:
                bx.draw(surface)
        if self.loaded['panel'] is not None:
            for pn in self.loaded['panel']:
                pn.render(surface)

    def back_is_clicked(self):
        ScenePlayer.pop()


