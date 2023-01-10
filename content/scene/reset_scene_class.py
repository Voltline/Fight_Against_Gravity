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


class ResetScene(Scene):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.check_code = ''

        labels = UI.new_reset_labels(self)  # label，分别为邮箱，密码，确认密码，验证码

        boxes = UI.new_reset_boxes(self)  # 输入框，分别为邮箱，密码，确认密码，验证码

        buttons = UI.new_reset_buttons(self)
        """显示验证码错误的panel"""
        self.close_button.r_xy = 0.88, 0.1
        self.wrong_check_box = MessageBox((0.5, 0.5), "警告", "验证码错误！")
        """显示没输入验证码的panel"""
        self.close_button.r_xy = 0.88, 0.1
        self.no_check_warning = MessageBox((0.5, 0.5), "警告", "获取验证码不成功，邮箱或用户名有误！")
        self.no_check_panel = Panel(self.reminder_panel_rect_small, '验证码为空', 22,
                                    [self.close_button])
        """显示没输入用户名的提示框"""
        self.empty_input_box_warning = MessageBox((0.5, 0.5), "警告", "以上输入框不得留空！")
        self.conflict_pwd_warning = MessageBox((0.5, 0.5), "警告", "两次密码输入不一致！")
        self.loaded = {'label': labels, 'box': boxes, 'button': buttons, 'panel': [], 'msgbox': []}
        self.bgm_id = 0

    def show(self):
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.screen.fill((10, 10, 10))
        pygame.draw.rect(self.screen, (46, 46, 46),
                         (self.width*0.25, self.height*0.20, self.width*0.5, self.height*0.6),
                         border_radius=15)
        self.draw_elements()
        pygame.display.flip()

    def reset_send_checkcode_clicked(self):
        username = self.loaded['box'][1].text
        # print(username)  # 测试用
        email = self.loaded['box'][0].text
        if username != '' and email != '':
            # 如果用户名和邮箱都不为空
            self.check_code = self.client.reset_get_checkcode(username, email)
            # 如果此处邮箱未注册，就弹出一个msgbox
        else:
            self.loaded['msgbox'] = [self.empty_input_box_warning]
            self.has_msgbox = True

    def confirm_reset_clicked(self):
        for box in self.loaded['box']:
            if box.text == '':
                self.loaded['msgbox'] = [self.empty_input_box_warning]
                # self.ban_inputbox()
                self.has_msgbox = True
                break

        if self.loaded['box'][2].text != self.loaded['box'][3].text:
            self.loaded['msgbox'] = [self.conflict_pwd_warning]
            self.has_msgbox = True
        elif self.check_code == '':
            # 未发送验证码
            self.loaded['msgbox'] = [self.no_check_warning]  # 12.28，为测试msgbox将此行右边的no_check_panel改了。
            # self.ban_inputbox()
            self.has_msgbox = True
        elif self.check_code.lower() != self.loaded['box'][4].text.lower():
            # 验证码错误
            self.loaded['msgbox'] = [self.wrong_check_box]
            # self.ban_inputbox()
            self.has_msgbox = True
        elif self.check_code.lower() == self.loaded['box'][4].text.lower():
            result = self.client.reset_push_password(
                self.loaded['box'][1].text,
                self.loaded['box'][0].text,
                self.check_code,
                self.loaded['box'][4].text,
                self.loaded['box'][2].text)
            if result:
                # print('success')
                self.reset_success_info = MessageBox((0.5, 0.5), "提示", "密码重置成功！")
                self.loaded['msgbox'] = [self.reset_success_info]
                self.has_msgbox = True
                ScenePlayer.pop()
            else:
                # print('fail', self.loaded['box'][1].text,
                #       self.loaded['box'][0].text,
                #       self.loaded['box'][2].text)
                self.reset_failed_msg_box = MessageBox((0.5, 0.5), "警告", "重置密码失败，请您稍后重试")
                self.loaded['msgbox'] = [self.reset_failed_msg_box]
                self.has_msgbox = True

    def close_is_clicked(self):
        self.loaded['panel'] = []
        self.box_is_able = True
