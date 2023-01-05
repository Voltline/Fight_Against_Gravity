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
        pygame.mixer.music.set_volume(0.3)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        # for i in range(10):
        #     pygame.time.delay(200)
        #     pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.03)
        while True:
            ScenePlayer.STACK[-1].update()
            ScenePlayer.STACK[-1].show()
            if pygame.mixer.music.get_busy():
                if (last_bgm_id == 0 or last_bgm_id == 2) and ScenePlayer.STACK[-1].bgm_id == 1:
                    # 停止当前播放的音乐
                    pygame.mixer.music.stop()
                    # 加载新的音乐文件
                    pygame.mixer.music.load(bgm_list[1])
                    # 播放新的音乐
                    pygame.mixer.music.play(-1)
                    last_bgm_id = 1
                elif (last_bgm_id == 1 or last_bgm_id == 2) and ScenePlayer.STACK[-1].bgm_id == 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(bgm_list[0])
                    pygame.mixer.music.play(-1)
                    last_bgm_id = 0
                elif ScenePlayer.STACK[-1].bgm_id == 2:
                    pygame.mixer.music.stop()
                    last_bgm_id = 2
            if not pygame.mixer.music.get_busy():
                if ScenePlayer.STACK[-1].bgm_id != 2:
                    pygame.mixer.music.load(bgm_list[ScenePlayer.STACK[-1].bgm_id])
                    pygame.mixer.music.play()

