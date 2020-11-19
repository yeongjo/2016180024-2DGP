from PicoModule import *
from GamePlay import *
import copy as cp

class Stair(DrawObj):

    # 중간 계단은 계단이 두개인데 서로 참조하고있어야 플레이어가 넘어갈수있게 만들어줄수있다.

    def __init__(self):
        super().__init__()
        self.load_img('img/stair.png')
        self.otherStair = None
        from Building import Building
        Building.stairs.append(self)

    def set_pos(self, x, y):
        self.pos = np.array([x + self.imgs[0].img.w / 2, y + self.imgs[0].img.h / 2])

    def check_player_pos(self, pos):
        _pos = self.pos - pos
        _len = sum(x * x for x in _pos)
        if _len < 15000:
            return True
        return False

    # 플레이어를 딴곳으로 보내줌
    def send_player(self, input_idx, my_idx):  # input_idx 0:w 1:a 2:s 3:d
        if input_idx == 0:
            if my_idx % 3 == 0 and my_idx < 12:
                return
            if my_idx >= 12 and my_idx % 3 == 0:
                Player.this.pos = cp.copy(Building.stairs[my_idx - 10].pos)
            else:
                Player.this.pos = cp.copy(Building.stairs[my_idx - 1].pos)
        elif input_idx == 2:
            if my_idx % 3 == 2 and my_idx >= 12:
                return
            if my_idx < 12 and my_idx % 3 == 2:
                Player.this.pos = cp.copy(Building.stairs[my_idx + 10].pos)
            else:
                Player.this.pos = cp.copy(Building.stairs[my_idx + 1].pos)

        elif input_idx == 1:
            if 6 <= my_idx <= 8 or 6 + 12 <= my_idx <= 8 + 12:  # 옆방으로
                Player.this.pos = cp.copy(Building.stairs[my_idx - 3].pos)
            else:
                Player.this.pos = cp.copy(self.pos)
                if 0 <= my_idx <= 2 or 0 + 12 <= my_idx <= 2 + 12:
                    pass
                else:
                    Player.this.pos[0] -= 150
                Player.this.is_in_stair = False
        elif input_idx == 3:
            if 3 <= my_idx <= 5 or 3 + 12 <= my_idx <= 5 + 12:  # 옆방으로
                Player.this.pos = cp.copy(Building.stairs[my_idx + 3].pos)
            else:
                Player.this.pos = cp.copy(self.pos)
                if 9 <= my_idx <= 11 or 9 + 12 <= my_idx <= 11 + 12:
                    pass
                else:
                    Player.this.pos[0] += 150
                Player.this.is_in_stair = False
        Player.this.pos[1] -= 95