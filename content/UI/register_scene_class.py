from content.UI.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.UI.scene_font import SceneFont
from content.UI.panel_class import Panel
from content.UI.scene_player_class import ScenePlayer
from Server import identify_client as ic
import os
import pygame


class RegScene(Scene):
    def __init__(self, setting):
        super().__init__(setting)
        self.identify_client = ic.createIdentifyClient()
        self.check_code = ''
        """label，分别为邮箱，用户名，密码，验证码"""
        r_email_label = Label(315, 180, 98, "请输入您的邮箱", SceneFont.r_font)
        r_id_label = Label(315, 260, 106, "请输入您的用户名", SceneFont.r_font)
        r_password_label = Label(315, 340, 42, "设置您的密码", SceneFont.r_font)
        r_check_label = Label(315, 420, 40, "验证码", SceneFont.r_font)
        labels = [r_email_label, r_id_label, r_password_label, r_check_label]
        """输入框，分别为邮箱，用户名，密码，验证码"""
        r_email_box = InputBox(pygame.Rect(450, 180, 350, 35))
        r_id_box = InputBox(pygame.Rect(450, 260, 350, 35))
        r_password_box = InputBox(pygame.Rect(450, 340, 350, 35))
        r_check_box = InputBox(pygame.Rect(450, 420, 350, 35))
        boxes = [r_email_box, r_id_box, r_password_box, r_check_box]

        r_rect = pygame.Rect(650, 500, 100, 40)
        r_button = Button("r", self.confirm_reg_clicked, r_rect,
                          self.setting.btbg_light, 0, '确认注册', SceneFont.log_font)
        r_button.add_img(self.setting.btbg_light_pressed)
        check_rect = pygame.Rect(430, 500, 110, 40)
        r_check_button = Button('check', self.send_checkcode_clicked, check_rect,
                                self.setting.btbg_light, 0, '发送验证码', SceneFont.log_font)
        r_check_button.add_img(self.setting.btbg_light_pressed)
        buttons = [r_button, r_check_button, self.back]
        """显示验证码错误"""
        self.wrong_check_panel = Panel(self.reminder_panel_rect_small, '验证码错误', 22, self.cancel_wrongcheck_clicked)
        self.loaded = {'label': labels, 'box': boxes, 'button': buttons, 'panel': []}
        """显示没输入验证码"""
        self.no_check_panel = Panel(self.reminder_panel_rect_small, '验证码为空(单击此处以继续)', 22, self.cancel_nocheck_clicked)

    def show(self, screen):
        screen.fill((10, 10, 10))
        pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        self.draw_elements(screen)
        pygame.display.flip()

    def confirm_reg_clicked(self):
        if self.check_code == '':
            self.loaded['panel'] = [self.no_check_panel]
            self.ban_inputbox()
        elif self.check_code.lower() != self.loaded['box'][3].text.lower():
            self.loaded['panel'] = [self.wrong_check_panel]
            self.ban_inputbox()
        elif self.check_code.lower() == self.loaded['box'][3].text.lower():
            result = self.identify_client.send_all_information(
                self.loaded['box'][1].text,
                self.loaded['box'][0].text,
                self.loaded['box'][2].text)
            if result:
                print('success')
                ScenePlayer.pop()
            else:
                print('fail', self.loaded['box'][1].text,
                      self.loaded['box'][0].text,
                      self.loaded['box'][2].text)

    def send_checkcode_clicked(self):
        username = self.loaded['box'][1].text
        print(username)  # 测试用
        email = self.loaded['box'][0].text
        self.check_code = self.identify_client.get_check_code(username, email)

    def cancel_wrongcheck_clicked(self):
        self.loaded['panel'] = []
        self.box_is_able = True
    def cancel_nocheck_clicked(self):
        self.loaded['panel'] = []
        self.box_is_able = True
