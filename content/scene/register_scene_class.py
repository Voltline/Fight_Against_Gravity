from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.UI.message_box import MessageBox
from content.UI.panel_class import Panel
from content.UI.ui_function import UIFunction as UI
from content.scene.scene_player_class import ScenePlayer
import pygame


class RegScene(Scene):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.check_code = ''

        labels = UI.new_reg_labels(self)  # label，分别为邮箱，用户名，密码，验证码

        boxes = UI.new_reg_boxes(self)  # 输入框，分别为邮箱，用户名，密码，验证码

        buttons = UI.new_register_buttons(self)
        """显示验证码错误的panel"""
        self.close_button.r_xy = 0.88, 0.1
        self.wrong_check_panel = Panel(self.reminder_panel_rect_small, '验证码错误', 22,
                                       [self.close_button])
        """显示没输入验证码的panel"""
        self.close_button.r_xy = 0.88, 0.1
        self.no_check_box = MessageBox((0.33, 0.4), (0.2, 0.15), "错误", "未输入验证码")  # 12/28,为测试msgbox添加
        self.no_check_panel = Panel(self.reminder_panel_rect_small, '验证码为空', 22,
                                    [self.close_button])
        self.loaded = {'label': labels, 'box': boxes, 'button': buttons, 'panel': [], 'msgbox': []}

    def show(self):
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.screen.fill((10, 10, 10))
        pygame.draw.rect(self.screen, (46, 46, 46),
                         (self.width*0.25, self.height*0.20, self.width*0.5, self.height*0.5),
                         border_radius=15)
        self.draw_elements()
        pygame.display.flip()

    def send_checkcode_clicked(self):
        username = self.loaded['box'][1].text
        print(username)  # 测试用
        email = self.loaded['box'][0].text
        self.check_code = self.client.register_get_checkcode(username, email)
        print(self.check_code)

    def confirm_reg_clicked(self):
        if self.check_code == '':
            self.loaded['msgbox'] = [self.no_check_box]  # 12.28，为测试msgbox将此行右边的no_check_panel改了。
            self.ban_inputbox()
        elif self.check_code.lower() != self.loaded['box'][3].text.lower():
            self.loaded['panel'] = [self.wrong_check_panel]
            self.ban_inputbox()
        elif self.check_code.lower() == self.loaded['box'][3].text.lower():
            result = self.client.register_push_password(
                self.loaded['box'][1].text,
                self.loaded['box'][0].text,
                self.check_code,
                self.loaded['box'][3].text,
                self.loaded['box'][2].text)
            if result:
                print('success')
                ScenePlayer.pop()
            else:
                print('fail', self.loaded['box'][1].text,
                      self.loaded['box'][0].text,
                      self.loaded['box'][2].text)

    def close_is_clicked(self):
        self.loaded['panel'] = []
        self.box_is_able = True
