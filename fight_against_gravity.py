import pygame
from pygame import Vector2
import threading  # 处理输入事件与绘制图形要和处理运动与碰撞分开，不然拖窗口会一起卡死

from all_settings import Settings
from content import game_function as gf
from content.game_manager import GameManager
from content.ship import Ship
from content.planet import Planet
from content.camera import Camera
import content.communicate_simulation as cs
from content.maps.map_obj import Map
from content.player_info import PlayerInfo

ip = '1.15.229.11'
port = 25555


def local_game():
    """本地游戏"""
    # 初始化游戏 并创建一个窗口
    pygame.init()
    settings = Settings()  # 初始化设置类
    icon = pygame.image.load(settings.icon_img_path)
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # 设置窗口大小
    pygame.display.set_caption(settings.game_title)  # 设置窗口标题

    # 设置gm (测试用)
    gm = GameManager(settings)
    ship1 = Ship(settings, Vector2(2240, 0), Vector2(0, -1100),
                 angle=0, player_name='1')
    ship2 = Ship(settings, Vector2(500, 0), Vector2(0, -900),
                 angle=3.14, player_name='2')
    gm.ships.add(ship1)
    gm.ships.add(ship2)
    planet1 = Planet(settings, Vector2(0, 0), Vector2(0, 60), mass=1e19)
    planet2 = Planet(settings, Vector2(2000, 0), Vector2(0, -600), mass=1e18)
    # planet3 = Planet(settings, Vector2(160000, 0), Vector2(0, 0.6), mass=1e23)

    gm.planets.add(planet1)
    gm.planets.add(planet2)
    # gm.planets.add(planet3)

    # 设置camera
    camera = Camera(screen, settings, ship1.player_name, gm.ships)
    traces = []  # 保存所有尾迹

    clock = pygame.time.Clock()  # 准备时钟
    printed_ms = 0  # 测试用，上次输出调试信息的时间
    physics_dt = settings.physics_dt
    surplus_dt = 0  # 这次delta_t被physics_dt消耗剩下的时间

    is_run = [True]
    while is_run[0]:
        delta_t = clock.tick(settings.max_fps) / 1000  # 获取delta_time(sec)并限制最大帧率
        now_ms = pygame.time.get_ticks()  # 测试用，当前时间
        if now_ms - printed_ms >= 2000:  # 每2秒输出一次fps等信息
            printed_ms = now_ms
            print('fps:', clock.get_fps())
            print('飞船信息:')
            for ship in gm.ships:
                print('\t', ship.player_name, ':', ship.hp, ship.loc, ship.spd.length())
            print('子弹总数:', len(gm.bullets))

        gf.check_events(settings, gm, camera, is_run)  # 检查键鼠活动

        surplus_dt += delta_t
        while surplus_dt >= physics_dt:
            surplus_dt -= physics_dt
            gm.check_collisions()
            gm.all_move(physics_dt)
            gf.ships_fire_bullet(settings, gm)
        gf.add_traces(settings, gm, traces, now_ms)

        surplus_ratio = surplus_dt / physics_dt
        gf.update_screen(settings, gm, camera, traces, surplus_ratio)




