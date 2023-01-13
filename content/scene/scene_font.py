import os

import pygame
import pygame.freetype


class SceneFont:

    log_font = {}
    white_font = {}
    white_font_msgbox = {}
    white_font_msgbox_title = {}
    menu_font = {}
    start_font = {}
    map_list_font = {}
    nickname_font = {}
    hp_value_font = {}
    red_font = {}
    big_red_font = {}
    user_name_font = {}
    ready_font = {}
    dready_font = {}
    """红色字体"""
    wating_font = {}
    wating_message_font = {}
    version_font = {}
    @staticmethod
    def init(scene_settings):
        """类变量初始化"""
        SceneFont.start_font = {
            'font': pygame.font.Font(scene_settings.font_path_light, 63),
            'tc': (36, 41, 47),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.log_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 22),
            'tc': (36, 41, 47),
            'bc': None,
            'align': 1,
            'valign': 1
        }  # 黑字用于白底
        SceneFont.white_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 16),
            'tc': (169, 183, 198),
            'bc': None,
            'align': 0,
            'valign': 0
        }  # 白字用于黑底
        SceneFont.white_font_msgbox = {
            'font': pygame.freetype.Font(scene_settings.font_path_normal, 19),
            'tc': (169, 183, 198),
            'bc': None,
            'align': 0,
            'valign': 0
        }  # msgbox正文字体
        SceneFont.white_font_msgbox_title = {
            'font': pygame.freetype.Font(scene_settings.font_path_normal, 25),
            'tc': (169, 183, 198),
            'bc': None,
            'align': 0,
            'valign': 0
        }  # msgbox正文字体

        SceneFont.menu_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 58),
            'tc': (36, 41, 47),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.map_list_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 25),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.nickname_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 12),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 0,
            'valign': 1
        }
        SceneFont.hp_value_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 9),
            'tc': (0, 0, 0),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.red_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 15),
            'tc': (255, 50, 80),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.big_red_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 35),
            'tc': (255, 50, 80),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.user_name_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 20),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 0,
            'valign': 1
        }
        SceneFont.dready_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 20),
            'tc': (255, 50, 80),
            'bc': None,
            'align': 0,
            'valign': 1
        }
        SceneFont.ready_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 20),
            'tc': (170, 200, 90),
            'bc': None,
            'align': 0,
            'valign': 1
        }
        SceneFont.set_title_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 25),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 0,
            'valign': 1
        }
        SceneFont.set_label_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 21),
            'tc': (169, 183, 198),
            'bc': None,
            'align': 0,
            'valign': 1
        }
        SceneFont.wating_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 60),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.wating_message_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 30),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        SceneFont.version_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 25),
            'tc': (255, 255, 255),
            'bc': None,
            'align': 0,
            'valign': 0
        }
        SceneFont.ping_good_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 16),
            'tc': (18, 230, 53),
            'bc': None,
            'align': 2,
            'valign': 1
        }
        SceneFont.ping_normal_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 16),
            'tc': (224, 135, 33),
            'bc': None,
            'align': 2,
            'valign': 1
        }
        SceneFont.ping_bad_font = {
            'font': pygame.font.Font(scene_settings.font_path_normal, 16),
            'tc': (209, 27, 27),
            'bc': None,
            'align': 2,
            'valign': 1
        }
