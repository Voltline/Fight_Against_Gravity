import os
import sys
import pygame


class ScenePlayer:
    STACK = []

    @staticmethod
    def push(scene):
        ScenePlayer.STACK.append(scene)

    @staticmethod
    def pop():
        ScenePlayer.STACK.pop()

    @staticmethod
    def show_scene():
        path = ScenePlayer.STACK[-1].path
        bgm_list = [path + "assets/sound/BGM/Deep_In_Space.wav",
                    path + "assets/sound/BGM/Free Game Music Song 1.wav"]
        pygame.mixer.music.load(bgm_list[0])
        last_bgm_id = 0
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        while True:
            ScenePlayer.STACK[-1].update()
            ScenePlayer.STACK[-1].show()
            if pygame.mixer.get_busy():
                if last_bgm_id == 0 and ScenePlayer.STACK[-1].bgm_id == 1:
                    # 停止当前播放的音乐
                    pygame.mixer.music.stop()
                    # 加载新的音乐文件
                    pygame.mixer.music.load(bgm_list[1])
                    # 播放新的音乐
                    pygame.mixer.music.play(-1)
                    last_bgm_id = 1
                if last_bgm_id == 1 and ScenePlayer.STACK[-1].bgm_id == 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(bgm_list[1])
                    pygame.mixer.music.play(-1)
                    last_bgm_id = 0