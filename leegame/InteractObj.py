from PicoModule import *
from GamePlay import *


class InteractObj(DrawObj):
    # doing_limit_time이 0 이상이면 키는 시간이 존재함
    g_id = 100

    def __init__(self, doing_limit_time=-1):
        super().__init__()
        GameManager.g_interactObjs.append(self)
        self.doing_limit_time = doing_limit_time  # 0 이상이면 키는 시간이 존재함
        self.is_playing_doing = False  # 플레이어가 키는시간이 있고 그 키는 시간중임을 표시
        self.name = ""
        self.id = InteractObj.g_id
        InteractObj.g_id += 1

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        tem_pos[1] += tem_size[1]//2
        fill_rectangle1(tem_pos, tem_size, 40, 40, 40)
        debug_text(str(self.pos), tem_pos)
        debug_text(str(self.name), tem_pos+np.array([0, 50]))

    # GameManager에서 서버로부터 들어온 패킷으로 불린다.
    def interact(self, player):
        self.name = player.name

    @classmethod
    def RESET(cls):
        cls.g_id = 100
