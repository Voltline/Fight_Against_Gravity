import os
import sys
import pygame
from content.UI.scene_settings import SceneSetting


class ScenePlayer:
    STACK = []

    @staticmethod
    def push(scene):
        ScenePlayer.STACK.append(scene)

    @staticmethod
    def pop():
        ScenePlayer.STACK.pop()

    def __init__(self, screen, setting):
        self.screen = screen
        self.check_code = ''
        self.setting = setting

    # def handle_event(self, e):
    #     check_code = ''
    #     if e.type == SceneEvents.LOGIN:
    #         userid = self.login.loaded['box'][0].text
    #         userpw = self.login.loaded['box'][1].text
    #         answer = self.ic.login(userid, userpw)
    #         if answer:
    #             print("登录成功")
    #             # self.push()  # 跳转游戏主界面
    #         else:
    #             print("failed")
    #     if e.type == SceneEvents.SENDCHECK:
    #         email = self.register.loaded['box'][0].text
    #         username = self.register.loaded['box'][1].text
    #         self.check_code = self.ic.get_check_code(username, email)
    #         print(self.check_code)
    #     if e.type == SceneEvents.SENDREGISTER:
    #         print(self.register.loaded['box'][3].text)
    #         if self.check_code != '':
    #             if self.check_code.lower() == self.register.loaded['box'][3].text.lower():
    #                 result = self.ic.send_all_information(self.register.loaded['box'][1].text,
    #                                                       self.register.loaded['box'][0].text,
    #                                                       self.register.loaded['box'][2].text
    #                                                       )
    #                 if result:
    #                     print('成功')
    #                     self.pop()
    #                     self.push(self.login)
    #                 else:
    #                     print("注册失败")
    #                     print(self.register.loaded['box'][1].text,
    #                           self.register.loaded['box'][0].text,
    #                           self.register.loaded['box'][2].text, )

    def show_scene(self):
        while True:
            for event in pygame.event.get():
                ScenePlayer.STACK[-1].update_event(event)
                # self.handle_event(event)  # 处理界面切换以外的事件
                # if event.type == SceneEvents.START:
                #     self.push(self.login)
                # if event.type == SceneEvents.REGISTER:
                #     self.push(self.register)
                # if event.type == SceneEvents.BACK:
                #     self.pop()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            ScenePlayer.STACK[-1].show(self.screen)


if __name__ == '__main__':
    pygame.init()
    scene_setting = SceneSetting()
    print(os.getcwd())
    sc = pygame.display.set_mode((1200, 800))
    s = ScenePlayer(sc, scene_setting)
    s.show_scene()
