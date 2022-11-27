import sys
import pygame
from pygame import Vector2
from content.trace import Trace
from content.ship import Ship
from content.planet import Planet
from content.msg_type import MsgType

# 鼠标位置信息，每帧实时更新
mouse_loc = Vector2(0, 0)
mouse_d_loc = Vector2(0, 0)


def check_events_keydown(event, settings, gm):
    """处理按下按键"""
    if event.key == settings.ship1_k_go_ahead:
        gm.ships.sprites()[0].is_go_ahead = True
    elif event.key == settings.ship1_k_go_back:
        gm.ships.sprites()[0].is_go_back = True
    elif event.key == settings.ship1_k_turn_left:
        gm.ships.sprites()[0].is_turn_left = True
    elif event.key == settings.ship1_k_turn_right:
        gm.ships.sprites()[0].is_turn_right = True
    elif event.key == settings.ship1_k_fire:
        gm.ships.sprites()[0].is_fire = True

    elif event.key == settings.ship2_k_go_ahead:
        gm.ships.sprites()[1].is_go_ahead = True
    elif event.key == settings.ship2_k_go_back:
        gm.ships.sprites()[1].is_go_back = True
    elif event.key == settings.ship2_k_turn_left:
        gm.ships.sprites()[1].is_turn_left = True
    elif event.key == settings.ship2_k_turn_right:
        gm.ships.sprites()[1].is_turn_right = True
    elif event.key == settings.ship2_k_fire:
        gm.ships.sprites()[1].is_fire = True


def check_events_keyup(event, settings, gm):
    """处理松开按键"""
    if event.key == settings.ship1_k_go_ahead:
        gm.ships.sprites()[0].is_go_ahead = False
    elif event.key == settings.ship1_k_go_back:
        gm.ships.sprites()[0].is_go_back = False
    elif event.key == settings.ship1_k_turn_left:
        gm.ships.sprites()[0].is_turn_left = False
    elif event.key == settings.ship1_k_turn_right:
        gm.ships.sprites()[0].is_turn_right = False
    elif event.key == settings.ship1_k_fire:
        gm.ships.sprites()[0].is_fire = False

    elif event.key == settings.ship2_k_go_ahead:
        gm.ships.sprites()[1].is_go_ahead = False
    elif event.key == settings.ship2_k_go_back:
        gm.ships.sprites()[1].is_go_back = False
    elif event.key == settings.ship2_k_turn_left:
        gm.ships.sprites()[1].is_turn_left = False
    elif event.key == settings.ship2_k_turn_right:
        gm.ships.sprites()[1].is_turn_right = False
    elif event.key == settings.ship2_k_fire:
        gm.ships.sprites()[1].is_fire = False


def check_events(settings, gm, camera, is_run):
    """响应键盘和鼠标事件"""
    global mouse_loc, mouse_d_loc
    mouse_loc.x, mouse_loc.y = pygame.mouse.get_pos()
    mouse_d_loc.x, mouse_d_loc.y = pygame.mouse.get_rel()

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
            check_events_keydown(event, settings, gm)
        elif event.type == pygame.KEYUP:
            check_events_keyup(event, settings, gm)

        event = pygame.event.poll()


def update_screen(settings, gm, camera, traces: list, surplus_ratio):
    """更新屏幕"""

    global mouse_loc

    # 重新绘制
    camera.screen.fill(settings.bg_color)  # 屏幕clear

    for objs in gm.ships, gm.bullets, gm.planets:
        for obj in objs:
            obj.rect.center = surplus_ratio*obj.loc + (1-surplus_ratio)*obj.loc0
    camera.move(mouse_loc)  # 要先更新飞船的rect再更新camera的位置

    # 先绘制尾迹，因为尾迹应该在最下层
    for trace in traces:
        trace.display(camera)

    for objs in gm.ships, gm.bullets, gm.planets:
        for obj in objs:
            obj.display(camera)
            obj.rect.center = obj.loc

    # 更新traces，删除其中应该消失的元素
    for trace in traces.copy():
        if trace.is_alive():
            break
        else:
            traces.remove(trace)

    # 刷新屏幕
    pygame.display.flip()


def ships_fire_bullet(settings, gm):
    for ship in gm.ships:
        if ship.is_alive and ship.is_fire:
            ship.fire_bullet(settings, gm.bullets)


def add_traces(settings, gm, traces, now_ms):
    """在traces里添加尾迹"""
    for objs in gm.ships, gm.planets:
        for obj in objs:
            traces.append(Trace(settings, obj.loc00, obj.loc, now_ms))
            obj.loc00.update(obj.loc)


def button_start_game_click(net, room_id, map_name, player_names):
    msg = {
        'type': MsgType.StartGame,
        'args': [room_id, map_name, player_names],
        'kwargs': {}
    }
    net.send(msg)


def get_time():
    """返回当前的时间(sec)"""
    return pygame.time.get_ticks()/1000


def find_player_ship(ships, player_name):
    """在ships中找player_name的ship，返回ship"""
    for ship in ships:
        if ship.player_name == player_name:
            return ship
    return None

