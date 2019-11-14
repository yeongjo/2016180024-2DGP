from PicoModule import *
from GamePlay import *


class InteractObj(DrawObj):



    # doing_limit_time이 0 이상이면 키는 시간이 존재함
    def __init__(self, doing_limit_time=-1):
        super().__init__()
        self.anim = Animator()
        # self.pos[1] = -139
        self.doing_remain_time = 0
        self.floor_y = None
        self.doing_limit_time = doing_limit_time  # 0 이상이면 키는 시간이 존재함
        self.is_playing_doing = False  # 플레이어가 키는시간이 있고 그 키는 시간중임을 표시
        self.damage = 0.01

        InteractObj.add_interact_obj(self)

    def tick(self, dt):
        self.anim.tick(dt)

        if self.is_playing_doing:
            self.doing_remain_time += dt
            if self.doing_limit_time < self.doing_remain_time and self.anim.anim_idx is not 1:
                self.is_playing_doing = False
                self.anim.play(1)
                from Player2 import Player2
                Player2.this.interact_obj = None
                GameManger.increase_player2_damage(self.damage)
                print("interactObj 32 : Player2.this interact!")

    def cancel_by_move(self):
        if not self.is_playing_doing:
            return

        from Player2 import Player2
        Player2.this.interact_obj = None
        self.doing_remain_time = 0
        self.is_playing_doing = False
        self.anim.play(0)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.pos), tem_pos)
        debug_text(str(self.floor_y), tem_pos + np.array([0, 20]))

    def interact(self, player_idx, is_interacting=False):
        if player_idx == 1 and self.anim.anim_idx is not 0:
            # Player1 Interact!!
            self.anim.play(0)
            GameManger.increase_player2_damage(-self.damage)
        elif player_idx == 2:
            if self.doing_limit_time >= 0 and self.anim.anim_idx is not 1:
                # Player2 Interacting~~
                self.anim.play(2)
                self.doing_remain_time = 0
                self.is_playing_doing = True
                from Player2 import Player2
                Player2.this.interact_obj = self
            elif self.anim.anim_idx is not 1:
                print("interact 63 : Player2 Interact!!")
                GameManger.increase_player2_damage(self.damage)
                self.anim.play(1)
            # else:
            #     self.anim.play(2)
            #     print('Player2.this interacting')

    # 이 오브젝트의 바닥위치 구하기
    def get_floor_pos(self):
        if self.floor_y is None:
            floor_offset = 0
            if self.pos[1] > MAP_HALF_HEIGHT:
                t_pos_y = self.pos[1] - MAP_HEIGHT
                floor_offset = MAP_HEIGHT
            else:
                t_pos_y = self.pos[1]
            # self.floor_y = floor_height[0]
            for t in EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING:
                self.floor_y = t + floor_offset
                if t <= t_pos_y:
                    break

        return np.array([self.pos[0], self.floor_y])

    def interact_input(self, player_idx, small_len):
        assert player_idx != 0, "player_idx != 0"
        if small_len < 150 * 150:
            self.interact(player_idx)

    interact_obj_list = []

    @classmethod
    def add_interact_obj(cls, interact_obj):
        cls.interact_obj_list.append(interact_obj)

    @classmethod
    def interact_to_obj(cls, player_idx):
        small_len_obj = None
        small_len = 300000000
        interact_obj_list = InteractObj.interact_obj_list
        for a in interact_obj_list:
            if player_idx == 1:
                _pos = mouse_pos_to_world(MouseController.pos, View.views[0])
                _pos[1] -= 150
            else:
                from Player2 import Player2
                _pos = Player2.this.pos
            _vec = _pos - a.get_floor_pos()
            _len = sum(x * x for x in _vec)
            if _len < small_len:
                small_len = _len
                small_len_obj = a

        if small_len_obj is not None:
            small_len_obj.interact_input(player_idx, small_len)