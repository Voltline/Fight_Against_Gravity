import pygame
from all_settings import Settings
import game_function as gf
from game_manager import GameManager
from time import sleep


def run_game():
    # 初始化游戏 并创建一个窗口
    pygame.init()
    settings = Settings()  # 初始化设置类
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # 设置窗口大小
    pygame.display.set_caption(settings.game_title)  # 设置窗口标题

    gm = GameManager(settings)

    pygame.display.set_caption('Fight Against Gravity')
    # 引入字体类型
    f = pygame.font.Font('assets/font/consolas.ttf', 50)
    # 生成文本信息，第一个参数文本内容；第二个参数，字体是否平滑；
    # 第三个参数，RGB模式的字体颜色；第四个参数，RGB模式字体背景颜色；
    text = f.render("Fight Against Gravity", True, (100, 30, 30), (0, 0, 0))
    # 获得显示对象的rect区域坐标
    text_rect = text.get_rect()
    # 设置显示对象居中
    text_rect.center = settings.screen_width/2, settings.screen_height/2
    # 将准备好的文本信息，绘制到主屏幕 Screen 上。
    screen.blit(text, text_rect)
    pygame.display.flip()
    sleep(settings.title_time_sec)

    # Main Loop
    while True:
        gf.check_events(settings, gm)

        gf.update_screen(settings, screen, gm)
