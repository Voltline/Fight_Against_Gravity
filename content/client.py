from Web.Modules.safeclient import SocketClient
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


def client_game(settings, screen, room_id, map_name, player_names):
    """在线游戏，本地端的游戏函数"""
    gm = GameManager()
    gf.load_map(settings, gm, Map(map_name), player_names)
    camera = Camera(screen, settings, PlayerInfo.player_name, gm.ships)
    traces = []

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

        # surplus_dt += delta_t
        # while surplus_dt >= physics_dt:
        #     surplus_dt -= physics_dt
        #     gf.check_collisions(gm)
        #     gf.all_move(gm, physics_dt)
        #     gf.ships_fire_bullet(settings, gm)
        gf.add_traces(settings, gm, traces, now_ms)

        surplus_ratio = surplus_dt / physics_dt
        gf.update_screen(settings, gm, camera, traces, surplus_ratio)


def client_main():
    # 初始化
    client = SocketClient(ip, port)
    pygame.init()
    settings = Settings()  # 初始化设置类
    icon = pygame.image.load(settings.icon_img_path)
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # 设置窗口大小
    pygame.display.set_caption(settings.game_title)  # 设置窗口标题

    # 开启一局游戏的步骤：
    # 房主点击开始游戏按钮，服务器收集{房间id,所有玩家id,地图名字}并调用创建游戏函数
    # 模拟时收集信息步骤省略

    # 登陆账号
    PlayerInfo.player_name = 'player1'

    # 在房间中，点击开始游戏按钮
    room_id = 1
    map_name = '静止双星系统'
    player_names = ['player1', 'player2']
    gf.button_start_game_click(room_id, map_name, player_names)

    # 游戏开始
    client_game(settings, screen, room_id, map_name, player_names)
