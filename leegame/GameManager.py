from PicoModule import *
from GamePlay import *

player2_multiply = 0
player1_multiply = 1.1

# 활성화 된 오브젝트 리스트를 가지고
# UI 상태 값에 업데이트 시켜준다.
class GameManager:
    __damage_remain_time = 1
    __damage_wait_time = 1

    __round_remain_time = 1
    __round_wait_time = 1

    __is_show_round_boardcast = False

    player1_win_count = 0
    player2_win_count = 0

    max_round_end_count = 2

    is_paused = False

    @classmethod
    def init(cls, player_uis):
        cls.mouseuser_ui, cls.keyuser_ui = player_uis
        cls.reset_game()

    @classmethod
    def update(cls, dt):
        if cls.__is_show_round_boardcast:
            return
        cls.__damage_remain_time -= dt
        if cls.__damage_remain_time <= 0:
            cls.__damage_remain_time += cls.__damage_wait_time
            cls.update_damage()

    @classmethod
    def increase_player2_damage(cls, damage):
        cls.keyuser_damage_amount += damage

    @classmethod
    def update_damage(cls):
        cls.mouseuser_ui.take_damage(cls.mouseuser_damage_amount + player1_multiply)
        cls.keyuser_ui.take_damage(cls.keyuser_damage_amount + player2_multiply)

    # UI에 수치가 있고 거기서 종료여부를 판단해서 받는다
    @classmethod
    def round_end(cls, idx):
        # TODO 게임 끝나는 상태로 변경
        if idx == 1:
            cls.player1_win_count += 1
            if cls.player1_win_count >= cls.max_round_end_count:
                cls.game_end(1)
            else:
                print("마우스 승리")
                cls.mouseuser_ui.boardcast(True)
        else:
            cls.player2_win_count += 1
            if cls.player2_win_count >= cls.max_round_end_count:
                cls.game_end(2)
            else:
                print("키보드 승리")
                cls.keyuser_ui.boardcast(True)

        cls.__is_show_round_boardcast = True
        cls.is_paused = True


    @classmethod
    def game_end(cls, idx):
        if idx == 1:
            print("마우스 승리 !!")
            cls.mouseuser_ui.boardcast(True, True)
        else:
            print("키보드 승리 !!")
            cls.keyuser_ui.boardcast(True, True)

    

    @classmethod
    def reset_round(cls):
        cls.mouseuser_damage_amount = 0.01  # 100초 초당한번씩하면
        cls.keyuser_damage_amount = 0  # 활성화된 오브젝트갯수에 따라 달라짐
        cls.mouseuser_ui.value = 1
        cls.mouseuser_ui.calculate_healthbar()
        cls.keyuser_ui.value = 1
        cls.keyuser_ui.calculate_healthbar()
        cls.__round_remain_time = cls.__round_wait_time
        cls.__damage_remain_time =  cls.__damage_wait_time
        cls.__is_show_round_boardcast = False
        cls.is_paused = False

        restart_game()


    @classmethod
    def reset_game(cls):
        cls.reset_round()
        cls.player1_win_count = 0
        cls.player2_win_count = 0


    @classmethod
    def end_boardcast(cls):
        cls.reset_round()
            