#show_HP：定义了一个函数用于显示血条以及血条的及时更新，以及飞机根据血条的多少有不同的样子


import pygame
def show_HP(ship s):
    now_blood= 100#_____#飞船当前血量
    max_blood= 100#_____#飞船本来的血量
    bp=now_blood/max_blood #血量百分比，用于画图
    return 0
    #hp=pygame.transform.chop(,())#裁剪血条，返回给hp,用来传给blit绘图
    #pygame.blit(hp)#看看是函数里画好还是返回hp的img对象
    #return hp
