import pygame
import sys
from Server.client_main import ClientMain
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.scene.scene_player_class import ScenePlayer
from content.scene.scene_font import SceneFont
from content.UI.panel_class import Panel
from content.UI.scrollable_panel_class import ScrollablePanel
from content.UI.ui_function import UIFunction as UIF
from content.UI.message_box import MessageBox


class Scene:
    screen = None
    settings = None
    client: ClientMain = None
    path = None

    def __init__(self):
        self.loaded = {'img': None, 'label': [], 'box': [], 'button': [], 'panel': [], 'msgbox': []}
        """全局组件，返回按钮、设置按钮、关闭按钮"""
        self.width = Scene.screen.get_rect().width
        self.height = Scene.screen.get_rect().height
        back_rect = pygame.Rect(20, 20, 45, 45)
        self.back = Button("back", self.back_is_clicked, back_rect, self.path + "assets\\Img\\back.png", 1)
        self.reminder_panel_rect = pygame.Rect(200, 300, 800, 200)
        self.reminder_panel_rect_small = pygame.Rect(450, 300, 300, 100)
        self.menu_like_panel_rect = pygame.Rect(300, 200, 600, 400)
        set_rect = pygame.Rect(0.4 * self.width, 0.6 * self.height, 290, 80)
        self.set_button = Button('setting', self.set_is_clicked, set_rect,
                                 self.path + "assets\\Img\\start_unpressed.png",
                                 0, '设置', SceneFont.start_font)
        self.set_button.add_img(self.path + "assets\\Img\\start_press.png")

        self.close_button = UIF.new_close_button(self)
        self.switcher = 0
        self.box_is_able = True
        """用于判断按下回车键时是否相应，如果是登录界面，敲下回车应该等同于登录，如果注册界面，敲下回车等同于进行注册"""
        self.id = 0  # 0对应未登录，1对应注册
        # msgbox优先级
        self.has_msgbox = False
        # 设置界面
        self.set_panel = UIF.new_setting_all_panel(self)
        self.set_panel.is_show = self.set_panel.is_able = False
        # 用于判断bgm如何播放, 0对应开始界面，注册登录界面，1对应房间大厅界面
        self.bgm_id = 0

    def ban_inputbox(self):
        """禁用输入框"""
        self.box_is_able = False

    def deal_event(self, e) -> bool:
        """将对应页面加载了的组件全部进行状态更新"""
        if self.loaded['panel'] is not None and not self.has_msgbox:
            for pn in self.loaded['panel'][::-1]:  # 越新的panel，响应的优先级越高
                if pn.update(e):
                    return True
        if self.loaded['button'] is not None and not self.has_msgbox:
            for bt in self.loaded['button']:
                if bt.update(e):
                    return True
        if self.loaded['box'] is not None and self.box_is_able and not self.has_msgbox:
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.loaded['box'])):
                    if self.loaded['box'][i].check_click(e):  # 若按下鼠标且位置在文本框
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
        if self.loaded['msgbox'] is not None:
            for mb in self.loaded['msgbox']:
                if mb.update(e, self):  # 此处将scene传入update，方便让msgbox来控制has_msgbox
                    return True
        return False

    def deal_events(self):
        """获取并处理所有消息"""
        for event in pygame.event.get():
            self.deal_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.deal_events()

    def draw_elements(self):
        if self.loaded['button'] is not None:
            for bt in self.loaded['button']:
                bt.render(self.screen)
        if self.loaded['label'] is not None:
            for lb in self.loaded['label']:
                lb.render(self.screen)
        if self.loaded['box'] is not None:
            for bx in self.loaded['box']:
                bx.render(self.screen)
        if self.loaded['panel'] is not None:
            for pn in self.loaded['panel']:
                pn.render(self.screen)
        if self.loaded['msgbox'] is not None:
            for mb in self.loaded['msgbox']:
                mb.render(self.screen)

    def back_is_clicked(self):
        ScenePlayer.pop()

    def set_is_clicked(self):
        if self.set_panel not in self.loaded['panel']:
            self.loaded['panel'].append(self.set_panel)
        self.set_panel.is_show = self.set_panel.is_able = True

    def set_key_clicked(self):
        new_key_set = (self.set_panel.loaded['ctrlrs'][-1]).loaded['boxes']
        new_ship1_keys = Scene.settings.ship1_keys.copy()
        for key in new_ship1_keys:
            new_ship1_keys[key] = Scene.settings.ship1_keys[key].copy()
        new_ship2_keys = Scene.settings.ship2_keys.copy()
        for key in new_ship2_keys:
            new_ship2_keys[key] = Scene.settings.ship2_keys[key].copy()
        labels = ['前进', '后退', '左转', '右转', '开火']

        all_keys = set()

        cnt = 0
        for box in new_key_set:
            if cnt < 5:
                new_ship1_keys[labels[cnt % 5]][1] = pygame.key.key_code(((box.text).replace(" ", "")).lower())
                all_keys.add(new_ship1_keys[labels[cnt % 5]][1])
            else:
                new_ship2_keys[labels[cnt % 5]][1] = pygame.key.key_code(((box.text).replace(" ", "")).lower())
                all_keys.add(new_ship2_keys[labels[cnt % 5]][1])
            cnt += 1

        # print(all_keys)

        if len(all_keys) == 10:
            if new_ship1_keys != Scene.settings.ship1_keys:
                Scene.settings.change_key("Ship1", list(new_ship1_keys.values()))
            if new_ship2_keys != Scene.settings.ship2_keys:
                Scene.settings.change_key("Ship2", list(new_ship1_keys.values()))
        else:
            show_duplicate_warning_msg_box = MessageBox((0.5, 0.5), "警告", "不要设置重复的按键！")
            self.loaded['msgbox'] = [show_duplicate_warning_msg_box]
            self.has_msgbox = True

        UIF.update_key_board(self, (self.set_panel.loaded['ctrlrs'][-1]).loaded['boxes'])

        self.set_close_is_clicked()

    def set_default(self):
        ship1_key = [["k_go_ahead", 119], ["k_go_back", 115], ["k_turn_left", 97],
                     ["k_turn_right", 100], ["k_fire", 101]]
        ship2_key = [["k_go_ahead", 105], ["k_go_back", 107], ["k_turn_left", 106],
                     ["k_turn_right", 108], ["k_fire", 117]]

        if list(Scene.settings.ship1_keys.values()) != ship1_key:
            Scene.settings.change_key("Ship1", ship1_key)

        if list(Scene.settings.ship2_keys.values()) != ship2_key:
            Scene.settings.change_key("Ship2", ship2_key)

        show_default_info_msg_box = MessageBox((0.5, 0.5), "提示", "键位已经恢复至默认布局！")
        self.loaded['msgbox'] = [show_default_info_msg_box]
        self.has_msgbox = True

        UIF.update_key_board(self, (self.set_panel.loaded['ctrlrs'][-1]).loaded['boxes'])

        self.set_close_is_clicked()

    def close_is_clicked(self):
        self.loaded['panel'].pop()

    def set_close_is_clicked(self):
        UIF.update_key_board(self, (self.set_panel.loaded['ctrlrs'][-1]).loaded['boxes'])
        self.set_panel.is_show = self.set_panel.is_able = False

    def quit_button_clicked(self):
        """点击暂停panel中的退出按钮"""
        ScenePlayer.pop()

    def show(self):
        pass

    def set_full_screen(self):
        Scene.settings.change_full_screen()
        confirm_full_screen_quit_btn = Button('重启', self.confirm_full_screen_quit, pygame.Rect(0, 0, 120, 40),
                                              Scene.settings.btbg_light, 0, '立即重启', SceneFont.log_font)
        confirm_full_screen_quit_btn.add_img(Scene.settings.btbg_light_pressed)
        cancel_full_screen_quit_btn = Button('取消', self.cancel_full_screen_quit, pygame.Rect(0, 0, 120, 40),
                                             Scene.settings.btbg_light, 0, '稍后重启', SceneFont.log_font)
        cancel_full_screen_quit_btn.add_img(Scene.settings.btbg_light_pressed)
        confirm_full_screen_quit_btn.r_xy = 0.08, 0.7
        cancel_full_screen_quit_btn.r_xy = 0.63, 0.7
        btns = [confirm_full_screen_quit_btn, cancel_full_screen_quit_btn]
        set_full_screen_ask_yesno_msg_box = MessageBox((0.5, 0.4),
                                                       "请确认", "切换至全屏需要重启游戏，是否现在重启？",
                                                       ctrlrs=btns, has_ctrlrs=True)
        self.loaded['msgbox'] = [set_full_screen_ask_yesno_msg_box]
        self.has_msgbox = True

    def confirm_full_screen_quit(self):
        self.loaded['msgbox'].pop()
        pygame.quit()
        sys.exit()

    def cancel_full_screen_quit(self):
        self.loaded['msgbox'].pop()

    @staticmethod
    def init(settings, screen, client):
        Scene.settings = settings
        Scene.path = settings.path
        Scene.screen = screen
        Scene.client = client
