import sys
import pygame
from pygame import Vector2


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


def check_events(settings, gm, camera):
    """响应键盘和鼠标事件"""
    global mouse_loc, mouse_d_loc
    mouse_loc.x, mouse_loc.y = pygame.mouse.get_pos()
    mouse_d_loc.x, mouse_d_loc.y = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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


def update_screen(settings, gm, camera, traces: list):
    """更新屏幕"""
    # 重新绘制
    camera.screen.fill(settings.bg_color)  # 屏幕clear

    # 先绘制尾迹，因为尾迹应该在最下层
    for trace in traces:
        trace.display(camera)

    for ship in gm.ships:
        if ship.is_alive:
            ship.display(camera)
    for bullet in gm.bullets:
        bullet.display(camera)
    for planet in gm.planets:
        planet.display(camera)

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


def all_move(gm, camera, delta_t):
    global mouse_loc
    camera.move(mouse_loc)
    for ship in gm.ships:
        if ship.is_alive:
            ship.move(delta_t, gm.planets)
    for bullet in gm.bullets:
        bullet.move(delta_t, gm.planets)
    for planet in gm.planets:
        planet.move(delta_t, gm.planets)


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


def get_all_loc(gm):
    """返回要绘制尾迹的对象的loc列表"""
    locs = []
    for space_obj in gm.ships:
        locs.append(space_obj.loc.copy())
    for space_obj in gm.planets:
        locs.append(space_obj.loc.copy())

    return locs
