# -*- coding: utf-8 -*-
import pygame
from content.UI.label_class import Label

'''
按钮控件，主体是一个承载图像的surface和一个承载文字的Label控件
本质上是一个响应鼠标点击的矩形区域
使用方法，制定好参数创建好一个Button，然后render即可
'''


class Control:
    def __init__(self, rect: pygame.Rect, img_file: str, img_sub: int, text, font_info, relate_xy=(0, 0)):
        """
        构造：
        rect: pygame.Rect对象,决定控制组件的位置,也用于创建label, img_file: 图片文件路径,img_sub: 表示这个图片有几张,
        text: 文本内容, font_info: 字体设置
        属性：is_show: 是否显示这个控件，is_active:控件是否被激活，is_able:控件是否可响应点击，
        status:用于标记这个按钮的状态，当一个按钮有多个状态时，status可用于索引对应素材。
        __img: 被加载好的图像，img_width:底图的长度，sub_img_width:子图宽度

        """
        self.is_show = 1
        self.is_active = 0
        self.is_able = 1
        self.status = 0
        self.rect = rect
        self.r_xy = relate_xy
        self.img_sub = img_sub
        self.text = text
        self.font_info = font_info

        # 下面来处理控制组建的图像，加载进去并形成一个list
        if img_file is None:
            self.__img = None
            self.img_width = 0
        else:
            self.__img = pygame.image.load(img_file)
            self.__img = pygame.transform.smoothscale(self.__img, (self.rect.width, self.rect.height))
            # self.__img = self.__img.convert_alpha()
            self.imgList = []
            self.imgList.append(self.__img)

        # 下面设定Label对象，对于纯图片的按钮，没有text，没有text就没有label
        if text is None:
            self.label = None
        else:
            self.label = Label(self.rect.left, self.rect.top, rect.width, text, font_info)

    def add_img(self, file_name: str):
        """多状态图进行添加"""
        img = pygame.image.load(file_name)
        img = pygame.transform.smoothscale(img, (self.rect.width, self.rect.height))
        img = img.convert_alpha()
        self.imgList.append(img)

    def render(self, surface):
        if self.is_show:
            if self.__img is not None:
                surface.blit(self.imgList[self.status], (self.rect.left, self.rect.top))
            if self.label is not None:
                self.label.set_pos(self.rect.left, self.rect.top, self.rect.height)
                self.label.render(surface)

    def is_over(self, point, pos_offset=(0, 0)) -> bool:
        """检测鼠标位置是否在按钮上，并检测按钮是否可用"""
        if self.is_able:
            flag = self.rect.collidepoint(point[0]-pos_offset[0], point[1]-pos_offset[1])
        else:
            flag = False
        return flag

    def check_click(self, event, pos_offset=(0, 0)) -> bool:
        """每次点击完返回是否被点到"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_over(event.pos, pos_offset)
        return False

    def check_move(self, event, pos_offset=(0, 0)):
        """如果鼠标在按钮上要响应相应的动态效果"""
        if event.type == pygame.MOUSEMOTION:
            if self.is_over(event.pos, pos_offset):
                self.status = 1
            else:
                self.status = 0

    def disable(self):
        # self.status = 0
        self.is_able = 0

    def enable(self):
        # self.status = 1
        self.is_able = 1

    def hide(self):
        self.is_show = 0

    def show(self):
        self.is_show = 1

    def change_image(self):
        if len(self.imgList) > 1:
            self.status = 1

    def update(self, event, pos_offset=(0, 0)) -> bool:
        """处理event，返回是否应该终止处理"""
        return False


class Button(Control):
    def __init__(self, name: str, clicked_function, rect, img_file, img_sub, text="", font_info=None):
        Control.__init__(self, rect, img_file, img_sub, text, font_info)

        self.name = name
        # self.event_id = event_id
        self.clicked_func = clicked_function

    def set_text(self, text):
        self.label.set_text(text)

    # update :按钮更新状态，并上传事件
    def update(self, event, pos_offset=(0, 0)) -> bool:
        if self.check_click(event, pos_offset):  # 响应点击
            print(self.name, "clicked")
            self.clicked_func()
            return True
            # data = {"from_ui": self.name, "status": self.status}
            # ev = pygame.event.Event(self.event_id, data)
            # pygame.event.post(ev)
        elif event.type == pygame.MOUSEMOTION:  # 响应鼠标移动
            if len(self.imgList) > 1:
                if self.is_over(event.pos, pos_offset):
                    self.status = 1
                else:
                    self.status = 0
        return False


class CheckBox(Control):
    def __init__(self, name, rect, img_file, img_sub, text, font_info):
        Control.__init__(self, rect, img_file, img_sub, text, font_info)

        self.name = name

        # 调整文字的位置,让文字在单选框左边
        if self.label is not None:
            x = rect.left + self.img_width
            y = rect.top + int(rect.height / 2)
            self.label.set_pos(x, y, 0, 1)

        self.status = 0

    def set_selected(self, flag):
        if flag:
            self.status = 2
        elif self.status > 0:
            self.status = 1

    def get_selected(self):
        return self.status == 0

    def update(self, event, pos_offset=(0, 0)) -> bool:
        if self.check_click(event, pos_offset):
            self.status = (self.status+1) % 2
            return True
        return False


class RadioButton(CheckBox):
    def __init__(self, group_id, btn_name, rect, img_file, img_sub, text, font_info):
        CheckBox.__init__(self, btn_name, rect, img_file, img_sub, text, font_info)
        RADIO_CHANGE = pygame.USEREVENT + 7

        self.group_id = group_id
        self.event_id = RADIO_CHANGE

    def change_selected(self, group_id, from_id):
        if self.group_id == group_id:
            self.set_selected(self.name == from_id)

    def update(self, event, pos_offset=(0, 0)) -> bool:
        if self.check_click(event, pos_offset):
            data = {"from_ui": self.name}
            ev = pygame.event.Event(self.event_id, data)
            pygame.event.post(ev)
            return True
        return False
