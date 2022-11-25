import sys
import pygame
from pygame import Vector2
from content.trace import Trace
from content.ship import Ship
from content.planet import Planet
from content.msg_type import MsgType
import content.communicate_simulation as cs

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


def all_move(gm, delta_t):
    for planet in gm.planets:
        planet.acc0.update(planet.acc)
        planet.update_loc(delta_t)
    for planet in gm.planets:
        planet.update_acc(gm.planets)
        planet.update_spd(delta_t)
    for ship in gm.ships:
        if ship.is_alive:
            ship.move(delta_t, gm.planets)
    for bullet in gm.bullets:
        bullet.move(delta_t, gm.planets)


def check_bullets_planets_collisions(gm):
    """使用圆形碰撞检测"""
    collections = pygame.sprite.groupcollide(
        gm.bullets, gm.planets, True, False, pygame.sprite.collide_circle)


def check_ships_bullets_collisions(gm):
    """mask检测"""
    collisions = pygame.sprite.groupcollide(
        gm.ships, gm.bullets, False, True, pygame.sprite.collide_mask)
    for ship, bullets in collisions.items():
        damage = 0
        for bullet in bullets:
            damage += bullet.damage
        ship.hit_bullet(damage, gm.ships, gm.dead_ships)


def check_ships_planets_collisions(gm):
    """mask检测"""
    collisions = pygame.sprite.groupcollide(
        gm.ships, gm.planets, False, False, pygame.sprite.collide_mask)
    for ship in collisions.keys():
        ship.die(gm.ships, gm.dead_ships)


def check_ships_ships_collisions(gm):
    """mask检测"""
    collisions = pygame.sprite.groupcollide(
        gm.ships, gm.ships, False, False, pygame.sprite.collide_mask)
    for ship1, ship2s in collisions.items():
        for ship2 in ship2s:
            if id(ship1) != id(ship2):
                ship1.die(gm.ships, gm.dead_ships)
                break


def check_collisions(gm):
    check_ships_ships_collisions(gm)
    check_ships_planets_collisions(gm)
    check_ships_bullets_collisions(gm)
    check_bullets_planets_collisions(gm)


def add_traces(settings, gm, traces, now_ms):
    """在traces里添加尾迹"""
    for objs in gm.ships, gm.planets:
        for obj in objs:
            traces.append(Trace(settings, obj.loc00, obj.loc, now_ms))
            obj.loc00.update(obj.loc)


def load_map(settings, gm, game_map, player_names):
    """加载地图到gm"""
    for group in gm.ships, gm.dead_ships, gm.planets, gm.bullets:
        group.clear()
    length = min(len(game_map.ships_info), len(player_names))
    for i in range(length):  # 加载飞船
        loc = game_map.ships_info[i].loc
        spd = game_map.ships_info[i].spd
        angle = game_map.ships_info[i].angle
        player_name = player_names[i]
        ship = Ship(settings, loc, spd, angle=angle, player_name=player_name)
        gm.ships.add(ship)
    for planet_info in game_map.planets_info:
        loc = planet_info.loc
        spd = planet_info.spd
        mass = planet_info.mass
        planet = Planet(settings, loc, spd, mass=mass)
        gm.planets.add(planet)


def button_start_game_click(room_id, map_name, player_names):
    msg_type = MsgType.StartGame
    cs.client_send(args=[msg_type, room_id, map_name, player_names])


def client_receive_msg(gm, is_run, room_id):
    msg = cs.client_receive()
    while msg:
        msg_args, msg_kwargs = msg[0], msg[1]
        if room_id == msg_args[1]:
            if msg_args[0] == MsgType.AllObjs:

            msg = cs.client_receive()


def client_receive_planets(gm, planets):
    for i in range(len(gm.planets)):
        gm.planets[i].loc.update(planets[i].loc)
        gm.planets[i].spd.update(planets[i].spd)
        gm.planets[i].acc.update(planets[i].acc)


def client_receive_ships(gm, ships, dead_ships):
    for dead_ship in dead_ships:
        for gm_ship in gm.ships:
            if gm_ship.
    for i in range(len(gm.ships)):
        gm.ships[i].loc.update(ships[i].loc)
        gm.ships[i].spd.update(ships[i].spd)
        gm.ships[i].acc.update(ships[i].acc)

def client_receive_bullets(gm, bullets):
    for i in range(len(gm.ships)):
        gm.bullets[i].loc.update(bullets[i].loc)
        gm.bullets[i].spd.update(bullets[i].spd)
        gm.bullets[i].acc.update(bullets[i].acc)


