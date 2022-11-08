import pygame
import pygame.key


class InputBox:
    def __init__(self, rect: pygame.Rect) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color(52, 52, 52)  # 未被选中的颜色
        self.color_active = pygame.Color(84, 82, 84)  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = ''
        self.done = False
        self.font = pygame.font.Font("Font/SourceHanSans-Normal.ttc", 18)
        self.font_color = pygame.Color(169, 183, 198)
        self.bg = pygame.Color(52, 52, 52)
        self.keylist = pygame.key.get_pressed()  # 获取所有案件，能够处理“按住”事件，而非单独单次的按住

    def deal_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.boxBody.collidepoint(event.pos):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_inactive
        if event.type == pygame.KEYDOWN:  # 键盘输入响应
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # elif event.key & pygame.KMOD_SHIFT:
                #     self.text += event.unicode
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txt_surface = self.font.render(self.text, True, self.font_color, self.bg)  # 文字转换为图片
        width = max(200, txt_surface.get_width()+10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        screen.blit(txt_surface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 3)
