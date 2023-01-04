import pygame.sprite
from pygame import Vector2
from typing import Tuple


class Camera:
    """控制玩家视角的类"""
    def __init__(self, settings, screen, player_ship=None):
        self.screen = screen
        self.loc: Vector2 = Vector2(0, 0)  # 位置
        self.zoom = 1  # 缩放程度
        self.move_spd = settings.camera_move_speed  # 移动速度系数(自由视角移动时)
        self.zoom_spd = settings.camera_zoom_speed  # 缩放速度系数
        self.zoom_max = settings.camera_zoom_max  # 缩放倍数上限(过高会导致fps过低)
        self.mode = 0  # 视角移动模式: 0:自由移动 1:跟随飞船
        self.mode_num = 2
        self.player_ship = player_ship  # 对应的玩家飞船
        self.d_loc = Vector2(0, 0)  # 鼠标上次移动的向量
        self.mouse_loc = Vector2(0, 0)  # 鼠标位置
        self.d_zoom = 0  # 鼠标滚轮上次移动的量

    def move(self):
        """视角的移动和缩放"""
        # 改变缩放
        if self.d_zoom != 0:
            zoom0 = self.zoom
            mouse_real_loc = Vector2(self.screen_to_real(self.mouse_loc))  # 鼠标对应的真实坐标
            self.zoom *= self.zoom_spd ** self.d_zoom
            if self.zoom > self.zoom_max:
                self.zoom = self.zoom_max
            self.loc += (mouse_real_loc - self.loc)*(1 - zoom0/self.zoom)
            self.d_zoom = 0

        # 改变位置
        if self.mode == 0:  # 自由移动模式
            self.loc += self.move_spd * self.d_loc / self.zoom
            self.d_loc.update(0, 0)
        elif self.mode == 1:  # 跟随飞船模式
            self.loc.update(self.player_ship.rect.center)

    def change_mode(self):
        if self.player_ship is not None:
            self.mode = (self.mode + 1) % self.mode_num

    def real_to_screen(self, obj_real_loc: Vector2) -> Tuple[float, float]:
        screen_center = self.screen.get_rect().center
        screen_x = screen_center[0] + (obj_real_loc.x - self.loc.x) * self.zoom
        screen_y = screen_center[1] + (obj_real_loc.y - self.loc.y) * self.zoom
        return screen_x, screen_y

    def screen_to_real(self, obj_screen_loc: Vector2) -> Tuple[float, float]:
        screen_center = self.screen.get_rect().center
        real_x = self.loc.x + (obj_screen_loc.x - screen_center[0])/self.zoom
        real_y = self.loc.y + (obj_screen_loc.y - screen_center[1])/self.zoom
        return real_x, real_y

    def blit(self, image, rect_real: pygame.Rect, loc_real: Vector2 = None):
        """
        image: 原始图片
        rect_real: 实际图片所在的rect
        loc_real: 图片rect的中心（rect是int的元组，不精确）；是None则还是使用rect_real.center
        功能：在self.screen的对应位置上绘制移动和缩放后的图片
        """
        rect_screen = pygame.rect.Rect(0, 0, rect_real.width*self.zoom, rect_real.height*self.zoom)
        if loc_real is not None:
            rect_screen.center = self.real_to_screen(loc_real)
        else:
            rect_screen.center = self.real_to_screen(Vector2(rect_real.center))
        self.screen.blit(pygame.transform.rotozoom(image.convert_alpha(), 0, self.zoom), rect_screen)

    def draw_dot(self, loc_real: Vector2, color):
        """
        loc_real: 实际坐标
        color: 点的颜色
        功能：在self.screen上对应实际loc的位置画一个颜色为color的点
        """
        pos_screen = list(map(int, self.real_to_screen(loc_real)))  # 转换后screen上的坐标，为二元组
        self.screen.set_at(pos_screen, color)

    def draw_line(self, loc0_real: Vector2, loc1_real: Vector2, color):
        pos0_screen = list(map(int, self.real_to_screen(loc0_real)))  # 转换后screen上的坐标，为二元组
        pos1_screen = list(map(int, self.real_to_screen(loc1_real)))
        pygame.draw.line(self.screen, color, pos0_screen, pos1_screen)

    def display_status_bar(self, status_bar, ship_loc_real: Vector2, ship_width):
        """显示飞船状态栏"""
        center_screen = self.real_to_screen(Vector2(ship_loc_real))
        ship_width *= self.zoom
        status_bar.set_left_top(center_screen[0]-ship_width/2,
                                center_screen[1]-ship_width/1.414-status_bar.hp_panel.rect.height*0.8)
        status_bar.render(self.screen)

