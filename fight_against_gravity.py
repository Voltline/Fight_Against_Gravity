import pygame
from pygame import Vector2

from all_settings import Settings
import game_function as gf
from game_manager import GameManager
from ship import Ship
from planet import Planet
from camera import Camera


def run_game():
    # 初始化游戏 并创建一个窗口
    pygame.init()
    settings = Settings()  # 初始化设置类
    icon = pygame.image.load(settings.icon_img_path)
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # 设置窗口大小
    pygame.display.set_caption(settings.game_title)  # 设置窗口标题

    # 设置gm (测试用)
    gm = GameManager(settings)
    ship1 = Ship(settings, Vector2(0, 0), Vector2(0, 800),
                 angle=0, player_name='1')
    ship2 = Ship(settings, Vector2(500, 0), Vector2(0, 900),
                 angle=3.14, player_name='2')
    gm.ships.add(ship1)
    gm.ships.add(ship2)
    planet1 = Planet(settings, Vector2(0, 0), Vector2(0, 0), mass=1e19)
    # planet2 = Planet(settings, Vector2(2000, 0), Vector2(0, -7), mass=1e19)
    # planet3 = Planet(settings, Vector2(106000, 0), Vector2(0, 0), mass=1e-30)

    gm.planets.add(planet1)
    # gm.planets.add(planet2)
    # gm.planets.add(planet3)

    # 设置camera
    camera = Camera(screen, settings, ship1.player_name, gm.ships)
    traces = []  # 保存所有尾迹

    # pygame.display.set_caption('Fight Against Gravity')
    # # 引入字体类型
    # f = pygame.font.Font('assets/font/consolas.ttf', 50)
    # # 生成文本信息，第一个参数文本内容；第二个参数，字体是否平滑；
    # # 第三个参数，RGB模式的字体颜色；第四个参数，RGB模式字体背景颜色；
    # text = f.render("Fight Against Gravity", True, (100, 30, 30), (0, 0, 0))
    # # 获得显示对象的rect区域坐标
    # text_rect = text.get_rect()
    # # 设置显示对象居中
    # text_rect.center = settings.screen_width/2, settings.screen_height/2
    # # 将准备好的文本信息，绘制到主屏幕 Screen 上。
    # screen.blit(text, text_rect)
    # pygame.display.flip()
    # sleep(settings.title_time_sec)

    # 准备时钟
    clock = pygame.time.Clock()

    # Main Loop
    while True:
        delta_t = clock.tick(settings.max_fps) / 1000  # 获取delta_time(sec)并限制最大帧率
        if (pygame.time.get_ticks()//10) % 500 == 0:  # 每5秒输出一次fps
            print('fps:', clock.get_fps())

        gf.check_events(settings, gm, camera)  # 检查键鼠活动
        gf.check_collisions(gm)
        gf.all_move(gm, camera, delta_t)
        gf.ships_fire_bullet(settings, gm)

        gf.update_screen(settings, gm, camera, traces)
