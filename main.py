#导入所需的模块
import sys
import pygame
# 使用pygame之前必须初始化
pygame.init()
# 设置主屏窗口
screen = pygame.display.set_mode((400,400))
# 设置窗口的标题，即游戏名称
pygame.display.set_caption('Fight Against Gravity')
# 引入字体类型
f = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',20)
# 生成文本信息，第一个参数文本内容；第二个参数，字体是否平滑；
# 第三个参数，RGB模式的字体颜色；第四个参数，RGB模式字体背景颜色；
text = f.render("Fight Against Gravity",True,(100,30,30),(0,0,0))
#获得显示对象的rect区域坐标
textRect =text.get_rect()
# 设置显示对象居中
textRect.center = (200,200)
# 将准备好的文本信息，绘制到主屏幕 Screen 上。
screen.blit(text,textRect)
# 固定代码段，实现点击"X"号退出界面的功能，几乎所有的pygame都会使用该段代码
while True:
    # 循环获取事件，监听事件状态
    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            #卸载所有模块
            pygame.quit()
            #终止程序，确保退出程序
            sys.exit()
    pygame.display.flip() #更新屏幕内容