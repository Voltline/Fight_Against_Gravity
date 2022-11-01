import sys
import pygame


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


def check_events(settings, gm):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        elif event.type == pygame.KEYDOWN:
            check_events_keydown(event, settings, gm)
        elif event.type == pygame.KEYUP:
            check_events_keyup(event, settings, gm)


def update_screen(settings, screen, gm):
    """更新屏幕"""
    # 重新绘制
    screen.fill(settings.bg_color)
    for ship in gm.ships:
        if ship.is_alive:
            ship.display()
    for bullet in gm.bullets:
        bullet.display()
    for planet in gm.planets:
        planet.display()

    # 刷新屏幕
    pygame.display.flip()


def ships_fire_bullet(settings, screen, gm):
    for ship in gm.ships:
        if ship.is_alive and ship.is_fire:
            ship.fire_bullet(settings, screen, gm.bullets)


def all_move(gm, delta_t):
    for ship in gm.ships:
        if ship.is_alive:
            ship.move(delta_t)
    for bullet in gm.bullets:
        bullet.move(delta_t)
    for planet in gm.planets:
        planet.move()


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
        gm.ships, gm.planets, False, True, pygame.sprite.collide_mask)
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
