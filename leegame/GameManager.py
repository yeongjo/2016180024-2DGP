from PicoModule import *
from GamePlay import *

player2_multiply = 1

# 활성화 된 오브젝트 리스트를 가지고
# UI 상태 값에 업데이트 시켜준다.
class GameManager:
    __remain_time = 1
    __wait_time = 1

    __scene_state = 1  # 게임화면

    player1_win_count = 0
    player2_win_count = 0

    round_end_count = 2

    @classmethod
    def init(cls, player_uis):
        cls.player_uis = player_uis
        cls.mouseuser_damage_amount = 0.01  # 100초 초당한번씩하면
        cls.keyuser_damage_amount = 0  # 활성화된 오브젝트갯수에 따라 달라짐

    @classmethod
    def update(cls, dt):
        if cls.__scene_state is not 1: return
        cls.__remain_time -= dt
        if cls.__remain_time <= 0:
            cls.__remain_time += cls.__wait_time
            cls.update_damage()

    @classmethod
    def increase_player2_damage(cls, damage):
        cls.keyuser_damage_amount += damage

    @classmethod
    def update_damage(cls):
        cls.player_uis[0].take_damage(cls.mouseuser_damage_amount)
        cls.player_uis[1].take_damage(cls.keyuser_damage_amount + player2_multiply)

    # UI에 수치가 있고 거기서 종료여부를 판단해서 받는다
    @classmethod
    def round_end(cls, idx):
        # TODO 게임 끝나는 상태로 변경
        if idx == 1:
            cls.player1_win_count += 1
            if cls.player1_win_count >= cls.round_end_count:
                cls.game_end(1)
            else:
                print("마우스 승리")
        else:
            cls.player2_win_count += 1
            if cls.player2_win_count >= cls.round_end_count:
                cls.game_end(2)
            else:
                print("키보드 승리")

    @classmethod
    def game_end(cls, idx):
        if idx == 1:
            print("마우스 승리 !!")
        else:
            print("키보드 승리 !!")
            