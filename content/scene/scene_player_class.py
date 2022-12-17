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
        while True:
            ScenePlayer.STACK[-1].update()
            ScenePlayer.STACK[-1].show()

