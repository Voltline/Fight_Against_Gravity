import pygame
from InputBox_Class import InputBox
from Button_class import Button
from Label_Class import Label
import sys
import os
from Web.在线验证部分.identify_client import IdentifyClient as ic
pygame.init()
screen = pygame.display.set_mode((1200, 800))
"""页面状态"""
page_status = 0

"""自定义事件"""
START = pygame.USEREVENT + 1
BACK = pygame.USEREVENT + 2
REGISTER = pygame.USEREVENT + 3
SENDREGISTER = pygame.USEREVENT + 4
LOGIN = pygame.USEREVENT + 5
SENDCHECK = pygame.USEREVENT + 6
# CONFIRM = pygame.USEREVENT + 7
SET = pygame.USEREVENT + 8
"""文件资源操作"""
current_work_directory = os.getcwd()  # 当前路径
print(current_work_directory)
fag_directory = os.path.dirname(current_work_directory)  # 上级路径
print(fag_directory)
"""开始游戏界面配置"""
start_font = {
    'font': pygame.font.Font("Font/SourceHanSans-Light.ttc", 65),
    'tc': (36, 41, 47),
    'bc': None,
    'align': 1,
    'valign': 1
}
start_rect = pygame.Rect(455, 300, 290, 100)

os.chdir(fag_directory)
start_title = pygame.image.load("assets/texture/FAGtitle.png")
start_title = pygame.transform.smoothscale(start_title, (514, 200))
start_title = start_title.convert_alpha()

os.chdir(current_work_directory)
start = Button("start", START, start_rect, "Img/start_unpressed.png", 1, 'Start', start_font)
start.add_img("Img/start_press.png")

"""返回按钮"""
back_rect = pygame.Rect(20, 20, 45, 45)
back = Button("back", BACK, back_rect, "Img/back.png", 1)

"""设置按钮"""
setting_rect = pygame.Rect(1100, 750, 48, 48)
setting = Button("setting", SET, setting_rect, "Img/setting_dark.png", 1)
"""登录界面"""
id_label = Label(330, 250, 98, "账号(用户名)")
password_label = Label(330, 350, 42, "密码")
id_box = InputBox(pygame.Rect(450, 250, 350, 35))  # 输入框的宽不由传入参数决定。
password_box = InputBox(pygame.Rect(450, 350, 350, 35))
boxL = [id_box, password_box]
"""注册按钮"""
register_rect = pygame.Rect(600, 450, 180, 40)
register_font = {
                'font': pygame.font.Font("Font/SourceHanSans-Normal.ttc", 22),
                'tc': (36, 41, 47),
                'bc': None,
                'align': 1,
                'valign': 1
            }
register_button = Button("register", REGISTER, register_rect, "Img/light_butbg.png", 0, '没有账号?注册', register_font)
"""登录按钮"""
login_rect = pygame.Rect(450, 450, 70, 40)
login_button = Button("login", LOGIN, login_rect, "Img/light_butbg.png", 0, "登录", register_font)
"""注册界面"""
r_font = {
            'font': pygame.font.Font("Font/SourceHanSans-Normal.ttc", 16),
            'tc': (169, 183, 198),
            'bc': None,
            'align': 0,
            'valign': 0
            }
r_email_label = Label(315, 180, 98, "请输入您的邮箱", r_font)
r_id_label = Label(315, 260, 106, "请输入您的用户名", r_font)
r_password_label = Label(315, 340, 42, "设置您的密码", r_font)
r_check_label = Label(315, 420, 40, "验证码", r_font)

r_email_box = InputBox(pygame.Rect(450, 180, 350, 35))
r_id_box = InputBox(pygame.Rect(450, 260, 350, 35))
r_password_box = InputBox(pygame.Rect(450, 340, 350, 35))
r_check_box = InputBox(pygame.Rect(450, 420, 350, 35))

r_rect = pygame.Rect(650, 500, 100, 40)
r_button = Button("r", SENDREGISTER, r_rect, "Img/light_butbg.png", 0, '确认注册', register_font)
check_rect = pygame.Rect(430, 500, 110, 40)
r_check_button = Button('check', SENDCHECK, check_rect, "Img/light_butbg.png", 0, '发送验证码', register_font)

# confirm_rect = pygame.Rect(430, 500, 80, 40)
# confirm_button = Button('confirm', CONFIRM, confirm_rect, "Img/light_butbg.png", 0, '确认', register_font)
"""注册测试"""
check_code = ''
identify_client = ic("47.100.69.244", 25555, "124.223.215.89", 25555)
running = True
while running:
    if page_status == 0:
        screen.fill((255, 255, 255))
    else:
        screen.fill((10, 10, 10))
    for event in pygame.event.get():
        if page_status == 0:  # 开始界面
            start.update(event)
            if start.check_move(event):
                start.status = 1
            else:
                start.status = 0
            if event.type == START:
                start.hide()
                print("clicked Start")
                start.disable()
                page_status += 1
        elif page_status == 1:
            id_box.deal_event(event)
            password_box.deal_event(event)
            back.update(event)
            register_button.update(event)
            login_button.update(event)
            if event.type == BACK:
                start.show()
                start.enable()
                page_status -= 1
            elif event.type == REGISTER:
                page_status += 1
                register_button.hide()
                register_button.disable()
                login_button.hide()
                login_button.disable()
                r_check_button.show()
                r_check_button.enable()
            elif event.type == LOGIN:
                userid = id_box.text
                userpw = password_box.text
                answer = identify_client.login(userid, userpw)
                if answer:
                    print("登录成功")
                else:
                    print("failed")

        elif page_status == 2:
            back.update(event)
            r_email_box.deal_event(event)
            r_id_box.deal_event(event)
            r_password_box.deal_event(event)
            r_check_box.deal_event(event)
            r_button.update(event)
            r_check_button.update(event)
            if event.type == BACK:
                page_status -= 1
                r_check_button.hide()
                r_check_button.disable()
                register_button.show()
                register_button.enable()
                login_button.show()
                login_button.enable()

            elif event.type == SENDREGISTER:
                print(check_code+'\n'+r_check_box.text)
                if check_code != '':
                    if check_code.lower() == r_check_box.text.lower():
                        result = identify_client.send_all_information(r_id_box.text, r_email_box.text, r_password_box.text)
                        if result:
                            print('成功')
                        else:
                            print("注册失败")
                print(r_email_box.text)
                print(r_id_box.text)
                print(r_password_box.text)
                # ic.send_all_information(r_email_box.text, r_id_box.text, r_password_box.text)
            elif event.type == SENDCHECK:  # 发送验证码
                username = r_id_box.text
                print(username)
                email = r_email_box.text
                check_code = identify_client.get_check_code(username, email)
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    if page_status == 0:
        screen.blit(start_title, (10, 10))
        start.render(screen)
    elif page_status == 1:
        pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        id_label.render(screen)
        password_label.render(screen)
        back.render(screen)
        id_box.draw(screen)
        password_box.draw(screen)
        register_button.render(screen)
        login_button.render(screen)
    elif page_status == 2:
        pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        back.render(screen)
        r_email_label.render(screen)
        r_id_label.render(screen)
        r_password_label.render(screen)
        r_check_label.render(screen)

        r_email_box.draw(screen)
        r_id_box.draw(screen)
        r_password_box.draw_password(screen)
        r_check_box.draw(screen)

        register_button.render(screen)
        r_button.render(screen)
        r_check_button.render(screen)
    setting.render(screen)
    pygame.display.flip()

