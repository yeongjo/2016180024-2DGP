from PicoModule import *
from GamePlay import *
from Player import Player


class InteractObj(DrawObj):
    # doing_limit_time이 0 이상이면 키는 시간이 존재함
    def __init__(self, doing_limit_time=-1):
        super().__init__()
        self.floor_y = None
        self.doing_limit_time = doing_limit_time  # 0 이상이면 키는 시간이 존재함
        self.is_playing_doing = False  # 플레이어가 키는시간이 있고 그 키는 시간중임을 표시

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        fill_rectangle(tem_pos, tem_size, 255, 0, 0)
        debug_text(str(self.pos), tem_pos)
        debug_text(str(self.floor_y), tem_pos + np.array([0, 20]))

    def interact(self, player_idx, is_interacting=False):
        if self.doing_limit_time >= 0:
            self.is_playing_doing = True
            Player.interact_obj = self

    # 이 오브젝트의 바닥위치 구하기
    def get_floor_pos(self):
        if self.floor_y is None:
            floor_offset = 0
            if self.pos[1] > MAP_HALF_HEIGHT:
                t_pos_y = self.pos[1] - MAP_HEIGHT
                floor_offset = MAP_HEIGHT
            else:
                t_pos_y = self.pos[1]
            for t in EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING:
                self.floor_y = t + floor_offset
                if t <= t_pos_y:
                    break

        return np.array([self.pos[0], self.floor_y])

    def reset(self):
        self.doing_remain_time = 0
        self.is_playing_doing = False
