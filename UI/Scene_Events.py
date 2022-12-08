import pygame


class SceneEvents:
    START = pygame.USEREVENT + 1
    BACK = pygame.USEREVENT + 2
    REGISTER = pygame.USEREVENT + 3
    SENDREGISTER = pygame.USEREVENT + 4
    LOGIN = pygame.USEREVENT + 5
    SENDCHECK = pygame.USEREVENT + 6
    LOCAL = pygame.USEREVENT + 7
    ONLINE = pygame.USEREVENT + 8
    SETTING = pygame.USEREVENT + 9