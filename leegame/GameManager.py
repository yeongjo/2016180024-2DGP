from PicoModule import *
import GamePlay
from UiScore import UiScore
import string
import random
import copy as cp

FURNITURE_START_IDX = 100

g_ui_scores = []
g_players = []
g_interactObjs = []
g_my_player_id = -1
g_win_player_idx = -1
g_players_name = []
make_player_queue = dict()


def init():
    from Player import Player
    from InteractObj import InteractObj
    global g_ui_scores, g_players, g_win_player_idx

    GamePlay.restart_game()

    g_win_player_idx = -1
    Player.RESET()
    InteractObj.RESET()

    for i in range(len(g_players) - 1):
        del (g_players[i])
        del (g_ui_scores[i])
    g_players = []
    g_ui_scores = []


def create_player(id, pos):
    if id not in make_player_queue.keys():
        print("add player queue id(", id,") (",pos,")")
        make_player_queue[id] = pos


def create_player_with_queue():
    from Player import Player
    global g_players_name, g_players
    for key, value in make_player_queue.items():
        # 이미 존재하는 플레이어면 만들지 않는다
        is_exist_player = False
        for player in g_players:
            if player.id == key:
                is_exist_player = True
                break
        if is_exist_player:
            continue

        # 존재하지 않는 플레이어면 만든다.
        name = ""
        while True:
            name = random.choice(string.ascii_lowercase)
            if name not in g_players_name:
                break
        g_players_name.append(name)
        g_ui_scores.append(UiScore(name))
        p = Player()
        p.init(name)
        p.id = key
        print("create player id ", p.id, " name: ", p.name)
        p.pos[0] = value[0]
        p.pos[1] = value[1]
        p.prev_pos = cp.copy(p.pos)
        g_players.append(p)


def update_player_pos(id, pos):
    while len(g_players) <= id:
        create_player(id, pos)

    for p in g_players:
        if p.id == id:
            p.update_pos(pos)
            return


def update():
    create_player_with_queue()


def update_interact_state(interactor_id, target_id):
    if target_id >= FURNITURE_START_IDX:  # 가구와의 상호작용
        interactor = None
        for t in g_players:
            if t.id == interactor_id:
                interactor = t
                interactor.interact()
                break
        for t in g_interactObjs:
            if t.id == target_id:
                t.interact(interactor)
                break
    else:
        interactor = None
        for t in g_players:
            if t.id == interactor_id:
                interactor = t
                break
        target = None
        for t in g_players:
            if t.id == target_id:
                target = t
                break
        interactor.attack()
        target.hit()


def set_my_player_id(id):
    global g_my_player_id
    g_my_player_id = id


# data = (12,43,53)
def update_ui(data):
    for i in range(len(g_ui_scores) - 1):
        g_ui_scores[i].value = data[i]
    g_ui_scores.sort(key=lambda x: x.value, reverse=True)
    for i in range(len(g_ui_scores) - 1):
        g_ui_scores[i].pos[1] = 10 + i * 30


def is_game_end():
    return g_win_player_idx != -1


def boardcast_win_player(win_player_idx):
    global g_win_player_idx
    import VictoryBoardcast
    VictoryBoardcast.end_boardcast()


def end_boardcast():
    GamePlay.restart_game()


def is_local_player_win():
    return g_win_player_idx == g_my_player_id
