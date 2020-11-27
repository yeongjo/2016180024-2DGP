from UiBoardcast import *
import GameManager
import copy as cp

def boardcast():
    view = View.active_view
    center = [view.half_w, view.half_h]
    img = Image()
    img.load("img/2_lose.png", 1)
    img.load("img/1_win.png", 0)
    VictoryBoardcast(img, center, 2.0)


def end_boardcast():
    view = View.active_view
    center = [view.half_w, view.half_h]
    img = Image()
    if GameManager.is_local_player_win():
        img.load("img/1_win.png", 0)
    else:
        img.load("img/2_lose.png", 1)
    EndVictoryBoardcast(img, center, 2.0)


class VictoryBoardcast(ImgBoardcast):
    def __init__(self, imgs, pos, remain_time=1.0):
        super().__init__(imgs, pos, remain_time)

    def exit(self):
        text = "졌"
        if GameManager.is_local_player_win():
            text = "이겼"
        RoundBoardcast(text, self.pos, 2.0)


class RoundBoardcast(TextBoardcast):
    def exit(self):
        print("round end")
        GameManager.end_boardcast()

    def render(self, cam):
        off = 300
        self.render_rect()
        import Font
        Font.active_font(1)
        pos = cp.copy(self.pos)
        pos[0] -= 50
        Font.draw_text('vs', pos, (230, 230, 230))
        Font.active_font(2)
        self.pos[0] -= off
        Font.draw_text(self.text, self.pos, (178, 27, 24))
        self.pos[0] += off + off
        Font.draw_text(self.text, self.pos, (87, 227, 210))
        self.pos[0] -= off


class EndVictoryBoardcast(VictoryBoardcast):
    def exit(self):
        text = "졌"
        if GameManager.is_local_player_win():
            text = "이겼"
        tem = EndRoundBoardcast(text, self.pos, 2.0)
        tem.alpha = int(self.alpha)

    def exit(self):
        print("last round end")
        GameManager.end_boardcast()

    def tick(self, dt):
        super().tick(dt)
        self.alpha += (255 - self.alpha) * 1 * dt
        if self.alpha > 255:
            self.alpha = 255


class EndRoundBoardcast(RoundBoardcast):
    def exit(self):
        print("last round end")
        GameManager.end_boardcast()
