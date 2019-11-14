from PicoModule import *
from GamePlay import *

class UiBoardcast(DrawObj):
    def __init__(self, pos, remain_time = 1.0):
        self.remain_time = remain_time
        super().__init__()
        self.pos = pos
        self.alpha = 100

    def exit(self):
        pass

    def tick(self, dt):
        self.remain_time -= dt
        if self.remain_time <= 0:
            self.exit()
            ObjsList.active_objs_list.remove_object(self)

    def render(self, cam):
        assert(True) # 상속받아서만 쓰기

    def render_rect(self):
        view = View.active_view
        fill_rectangle(0,0,view.w, view.h,0,0,0,int(self.alpha))


class ImgBoardcast(UiBoardcast):

    def __init__(self, imgs, pos, remain_time = 1.0):
        super().__init__(pos,remain_time)
        self.imgs = imgs

    def render(self, cam):
        self.render_rect()
        self.imgs[cam.idx].render(self.pos, self.size)

class TextBoardcast(UiBoardcast):
    def __init__(self, text, pos, remain_time = 1.0):
        super().__init__(pos, remain_time)
        self.text = text


    def render(self, cam):
        view = View.active_view
        fill_rectangle(0,0,view.w, view.h,0,0,0,int(self.alpha))
        import Font
        Font.active_font(2)
        Font.draw_text(self.text, self.pos)