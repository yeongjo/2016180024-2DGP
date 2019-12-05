from PicoModule import *
from Sound import Sound


class Button(DrawObj):

    def __init__(self, x, y, x2, y2, text, func):
        super().__init__()
        self.pos[0] = x
        self.pos[1] = y
        self.x2 = x2
        self.y2 = y2
        self.text = text
        self.fucn = func
        self.is_clicked = False
        # self.pop_sound = Sound.load('sound/Pop.wav', 100)

    def tick(self, dt):
        if MouseController.is_down and not self.is_clicked:
            mx = MouseController.pos[0]
            my = MouseController.pos[1]
            x = self.pos[0]
            y = self.pos[1]
            x2 = self.x2
            y2 = self.y2
            if collide_rect_point((x,y2,x2,y),(mx,my)):
                self.is_clicked = True
                # self.pop_sound.play()
                self.fucn()
        else:
            self.is_clicked = False

    def render(self, cam):
        #tem_pos, tem_size = self.calculate_pos_size(cam)
        # x = tem_pos[0]
        # y = tem_pos[1]
        x = self.pos[0]
        y = View.active_view.h - self.pos[1]
        w = self.x2
        h = View.active_view.h - self.y2
        fill_rectangle(x,y,w,h,30,30,30)

        import Font
        Font.active_font(3)
        Font.draw_text(self.text, (x, y-40))

