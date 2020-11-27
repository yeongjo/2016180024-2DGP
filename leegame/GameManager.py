from PicoModule import *
import GamePlay
from UiScore import UiScore
import string
import random
import copy as cp
import game_framework

FURNITURE_START_IDX = 100

g_players_and_scores = dict()
g_interactObjs = []
g_my_player_id = -1
g_win_player_idx = -1
g_players_name = []
make_player_queue = dict()


def init():
    from Player import Player
    from InteractObj import InteractObj
    global g_players_and_scores, g_win_player_idx

    GamePlay.restart_game()

    g_win_player_idx = -1
    Player.RESET()
    InteractObj.RESET()

    g_players_and_scores.clear()


def create_player(id, pos):
    if id not in make_player_queue.keys():
        print("add player queue id(", id, ") (", pos, ")")
        make_player_queue[id] = pos


def get_random_name(idx):
    name = "p"+str(idx)
    # for i in range(idx - len(g_players_name) + 1):
    #     while True:
    #         name = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
    #         if name not in g_players_name:
    #             break
    #     g_players_name.append(name)
    return name


def create_player_with_queue():
    from Player import Player
    global g_players_name, g_players_and_scores
    item = cp.copy(make_player_queue)
    for key, value in item.items():
        # 이미 존재하는 플레이어면 만들지 않는다
        if key in g_players_and_scores.keys():
            continue
        # is_exist_player = False
        # for player in g_players_and_scores:
        #     if player.id == key:
        #         is_exist_player = True
        #         break
        # if is_exist_player:
        #     continue

        # 존재하지 않는 플레이어면 만든다.

        # 이름 만들기
        name = get_random_name(key)

        p = Player()
        p.init(name)
        p.id = key
        print("create player id ", p.id, " name: ", p.name)
        p.pos[0] = value[0]
        p.pos[1] = value[1]
        p.prev_pos = cp.copy(p.pos)
        g_players_and_scores[key] = [p, UiScore(name)]
    reset_ui()


def update_player_pos(id, pos):
    create_player(id, pos)

    for p, s in g_players_and_scores.values():
        if p.id == id:
            p.update_pos(pos)
            return


def update():
    create_player_with_queue()


def update_interact_state(interactor_id, target_id):
    if target_id >= FURNITURE_START_IDX:  # 가구와의 상호작용
        interactor = None
        for t, s in g_players_and_scores.values():
            if t.id == interactor_id:
                interactor = t
                interactor.interact()
                break
        for t in g_interactObjs:
            if t.id == target_id:
                t.interact(interactor)
                break
    else:
        for t, s in g_players_and_scores.values():
            if t.id == interactor_id:
                t.attack()
                break
        for t, s in g_players_and_scores.values():
            if t.id == target_id:
                t.hit()
                break


def set_my_player_id(id):
    global g_my_player_id
    g_my_player_id = id


def reset_ui():
    update_ui([])


# data = (12,43,53)
def update_ui(data):
    for i in range(len(data)):
        if i in g_players_and_scores.keys():
            g_players_and_scores[i][1].value = data[i]

    scores = [value[1] for value in g_players_and_scores.values()]
    scores.sort(key=lambda x: x.value, reverse=True)
    for i in range(len(scores)):
        scores[i].pos[1] = View.active_view.h - 100 - i * 100


def is_game_end():
    return g_win_player_idx != -1


def boardcast_win_player(win_player_idx):
    global g_win_player_idx
    import VictoryBoardcast
    g_win_player_idx = win_player_idx
    VictoryBoardcast.end_boardcast()


def end_boardcast():
    import game_framework
    import GameEndScene
    game_framework.change_state(GameEndScene)


def is_local_player_win():
    return g_win_player_idx == g_my_player_id


def end_game():
    game_framework.quit()
