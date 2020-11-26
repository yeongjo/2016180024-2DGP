from PicoModule import *
import GamePlay
from UiScore import UiScore
import string
import random

FURNITURE_START_IDX = 100

g_ui_scores = []
g_players = []
g_interactObjs = []
g_my_player_id = -1
g_win_player_idx = -1
g_player_cnt = 0


def init():
    from Player import Player
    from InteractObj import InteractObj
    global g_ui_scores, g_players, g_player_cnt

    GamePlay.restart_game()
    g_win_player_idx = -1
    Player.RESET()
    InteractObj.RESET()

    for i in range(len(g_players) - 1):
        del (g_players[i])
        del (g_ui_scores[i])
    g_players = []
    g_ui_scores = []

    name = set()
    while len(name) < g_player_cnt:
        name.add(random.choice(string.ascii_lowercase))
    for i in range(g_player_cnt):
        g_ui_scores.append(UiScore(name.pop()))
        p = Player()
        p.init(name)
        g_players.append(p)


def update_player_pos(id, pos):
    for p in g_players:
        if p.id == id:
            p.pos[0] = pos[0]
            p.pos[1] = pos[1]
            return


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
    g_ui_scores.sort(key=lambda x: g_ui_scores[x].value, reverse=True)
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
