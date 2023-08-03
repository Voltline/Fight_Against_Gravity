import pygame
import time

pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
key = joystick.get_init()
print('ready____________________________')
print(key)
name = joystick.get_name()
print('name____________________________')
print(name)
axes = joystick.get_numaxes()
print('axes________________________')
print(axes)

buttons = joystick.get_numbuttons()  # 获得 Joystick 上按钮的数量
print('buttons_______________________')
print(buttons)

while 1:
    for event_ in pygame.event.get():
        if event_.type == pygame.JOYHATMOTION:
            if joystick.get_hat(0) and event_.dict['value'] != (0, 0):
                loc = event_.dict['value']
                if loc[0] != 0:
                    if loc[0] == 1:
                        print("Right", end = '')
                    else:
                        print("Left", end = '')
                if loc[1] != 0:
                    if loc[1] == 1:
                        print("Up", end = '')
                    else:
                        print("Down", end = '')
                print()

        if event_.type == pygame.JOYBUTTONDOWN or event_.type == pygame.JOYBUTTONUP:
            if joystick.get_button(0):
                print('A')
            if joystick.get_button(1):
                print('B')
            if joystick.get_button(2):
                print('X')
            if joystick.get_button(3):
                print('Y')
            if joystick.get_button(4):
                print('L')
            if joystick.get_button(5):
                print('R')
            if joystick.get_button(6):
                print('Manage Interface')
            if joystick.get_button(7):
                print('Settings')
            if joystick.get_button(8):
                print('LeftStick')
            if joystick.get_button(9):
                print('RightStick')
        if event_.type == pygame.JOYAXISMOTION:
            print(joystick.get_axis(1), joystick.get_axis(3), joystick.get_button(5))