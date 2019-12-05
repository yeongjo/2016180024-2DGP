from PicoModule import *
from GamePlay import *
from VictoryBoardcast import VictoryBoardcast
from VictoryBoardcast import EndVictoryBoardcast

class PlayerUI(DrawObj):

    def __init__(self, l):
        super().__init__(l)

    # idx: -1, 1 (-1이 키보드 유저)
    def init(self, r, g, b, idx, side_img_pos):
        self.color = (r, g, b)
        self.idx = idx
        self.__hp_max_x = 369 * idx
        self.value = 1
        self.side_img_pos = side_img_pos
        self.win_count = 0
        self.imgs = [Image(), Image()]

        if idx == 1:
            View.views[0].use()
            self.imgs[0].load("img/1_win.png", 0)
            View.views[1].use()
            self.imgs[1].load("img/2_lose.png", 1)
        else:
            View.views[0].use()
            self.imgs[0].load("img/1_lose.png", 0)
            View.views[1].use()
            self.imgs[1].load("img/2_win.png", 1)

        self.calculate_healthbar()

    def render(self, cam):
        tem_pos = self.tem_pos
        tem_size = self.tem_size
        fill_rectangle(tem_pos[0], tem_pos[1], tem_size[0], tem_size[1], self.color[0], self.color[1],
                              self.color[2])
        # draw_text(str(self.win_count), tem_pos)

    def calculate_healthbar(self):
        self.side_img_pos[0] = self.value * self.__hp_max_x + self.idx * -3

        view = View.active_view
        vw = view.half_w
        vh = view.h
        ratio1 = view.w / MAP_WIDTH

        self.tem_size = np.array([self.size[0] * ratio1 + vw, vh - self.size[1] * ratio1])
        self.tem_pos = np.array([self.value * self.__hp_max_x * ratio1 + vw, vh - self.pos[1] * ratio1])

    # 밖으로 빼야되는데 너무 귀찮다
    def take_damage(self, amount):
        self.value -= amount
        if self.value <= 0:
            self.value = 0

        self.calculate_healthbar()

        if self.value <= 0:
            # call end
            GameManager.round_end(self.idx)

    def boardcast(self,is_win, is_end=False):
        view = View.active_view
        center = [view.half_w, view.half_h]
        if is_end:
            EndVictoryBoardcast(self.imgs, center, 3.0)
        else:
            VictoryBoardcast(self.imgs, center, 2.0)
