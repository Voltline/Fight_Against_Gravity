import sys
import pygame
from pygame import Vector2
from content.local.trace import Trace
from Server.Modules.OptType import OptType

# 鼠标位置信息，每帧实时更新
mouse_loc = Vector2(0, 0)
mouse_d_loc = Vector2(0, 0)


def check_events_keydown(event, settings, ship1, ship2):
    """处理按下按键"""
    if event.key == settings.ship1_k_go_ahead:
        ship1.is_go_ahead = True
    elif event.key == settings.ship1_k_go_back:
        ship1.is_go_back = True
    elif event.key == settings.ship1_k_turn_left:
        ship1.is_turn_left = True
    elif event.key == settings.ship1_k_turn_right:
        ship1.is_turn_right = True
    elif event.key == settings.ship1_k_fire:
        ship1.is_fire = True

    elif event.key == settings.ship2_k_go_ahead:
        ship2.is_go_ahead = True
    elif event.key == settings.ship2_k_go_back:
        ship2.is_go_back = True
    elif event.key == settings.ship2_k_turn_left:
        ship2.is_turn_left = True
    elif event.key == settings.ship2_k_turn_right:
        ship2.is_turn_right = True
    elif event.key == settings.ship2_k_fire:
        ship2.is_fire = True


def check_events_keyup(event, settings, ship1, ship2):
    """处理松开按键"""
    if event.key == settings.ship1_k_go_ahead:
        ship1.is_go_ahead = False
    elif event.key == settings.ship1_k_go_back:
        ship1.is_go_back = False
    elif event.key == settings.ship1_k_turn_left:
        ship1.is_turn_left = False
    elif event.key == settings.ship1_k_turn_right:
        ship1.is_turn_right = False
    elif event.key == settings.ship1_k_fire:
        ship1.is_fire = False

    elif event.key == settings.ship2_k_go_ahead:
        ship2.is_go_ahead = False
    elif event.key == settings.ship2_k_go_back:
        ship2.is_go_back = False
    elif event.key == settings.ship2_k_turn_left:
        ship2.is_turn_left = False
    elif event.key == settings.ship2_k_turn_right:
        ship2.is_turn_right = False
    elif event.key == settings.ship2_k_fire:
        ship2.is_fire = False


def check_events(settings, ship1, ship2, camera, is_run):
    """响应键盘和鼠标事件"""
    global mouse_loc, mouse_d_loc
    mouse_loc.x, mouse_loc.y = pygame.mouse.get_pos()
    mouse_d_loc.x, mouse_d_loc.y = pygame.mouse.get_rel()
    camera.mouse_loc.update(mouse_loc)

    event = pygame.event.poll()
    while event:
        if event.type == pygame.QUIT:
            is_run[0] = False
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # 是否按下鼠标中键
                camera.change_mode()
        elif event.type == pygame.MOUSEMOTION:
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[2]:  # 如果鼠标右键被按下
                camera.d_loc.update(mouse_d_loc)
        elif event.type == pygame.MOUSEWHEEL:
            camera.d_zoom = event.y

        elif event.type == pygame.KEYDOWN:
            check_events_keydown(event, settings, ship1, ship2)
        elif event.type == pygame.KEYUP:
            check_events_keyup(event, settings, ship1, ship2)

        event = pygame.event.poll()


def update_screen(settings, gm, camera, traces: list, surplus_ratio, now_sec=-1):
    """更新屏幕"""
    # 重新绘制
    camera.screen.fill(settings.bg_color)  # 屏幕clear

    for objs in gm.ships, gm.bullets, gm.planets:
        for obj in objs:
            obj.rect.center = surplus_ratio*obj.loc + (1-surplus_ratio)*obj.loc0
    camera.move()  # 要先更新飞船的rect再更新camera的位置

    # 先绘制尾迹，因为尾迹应该在最下层
    for trace in traces:
        trace.display(camera)

    for objs in gm.bullets, gm.planets, gm.ships:
        for obj in objs:
            obj.display(camera)
            obj.rect.center = obj.loc

    # 最后画爆炸，因为爆炸应该在最上层
    for ship in gm.dead_ships:
        ship.update_explosion_image(now_sec)
        ship.display(camera)

    # 更新traces，删除其中应该消失的元素
    for trace in traces[:]:
        if trace.is_alive(now_sec):
            break
        else:
            traces.remove(trace)
    # 刷新屏幕在scene中完成


def add_traces(settings, gm, traces, now_sec):
    """在traces里添加尾迹"""
    for objs in gm.ships, gm.planets:
        for obj in objs:
            traces.append(Trace(settings, obj.loc00, obj.loc, now_sec))
            obj.loc00.update(obj.loc)


def button_start_game_click(net, room_id, map_name, player_names):
    msg = {
        'opt': OptType.StartGame,
        'time': get_time(),
        'args': [room_id, map_name, player_names],
        'kwargs': {}
    }
    net.send(msg)


def get_time():
    """返回当前的时间(sec)"""
    return pygame.time.get_ticks()/1000


def find_player_ship(ships, player_name):
    """在ships中找player_name的ship，返回ship"""
    if ships:
        for ship in ships:
            if ship.player_name == player_name:
                return ship
    return None


def init_pygame_window(settings=None) -> pygame.Surface:
    """初始化pygame窗口，返回screen"""
    pygame.init()
    if settings is not None:
        icon = pygame.image.load(settings.icon_img_path)
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # 设置窗口大小
        pygame.display.set_caption(settings.game_title)  # 设置窗口标题
        return screen
    else:
        pygame.display.set_mode((20, 20))
        return None
