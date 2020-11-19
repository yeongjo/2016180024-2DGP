from PicoModule import *
import GamePlay
from UiScore import UiScore
import string
import random


ui_scores = []
players = []
my_player_id = -1


def init(player_cnt):
    from Player import Player
    global ui_scores, players

    GamePlay.restart_game()
    Player.g_id = 0

    for i in range(len(players)-1):
        del (players[i])
        del (ui_scores[i])
    players = []
    ui_scores = []

    name = set()
    while len(name) < player_cnt:
        name.add(random.choice(string.ascii_lowercase))
    for i in range(player_cnt):
        ui_scores.append(UiScore(name.pop()))
        p = Player()
        p.init(name)
        players.append(p)


def update_player_pos(id, pos):
    for p in players:
        if p.id == id:
            p.pos[0] = pos[0]
            p.pos[1] = pos[1]
            return


def update_interact_state(interactor_id, target_id):
    if target_id >= 100: # 가구와의 상호작용
        pass


def set_my_player_id(id):
    global my_player_id
    my_player_id = id


# data = (12,43,53)
def update_ui(data):
    for i in range(len(ui_scores) - 1):
        ui_scores[i].value = data[i]
    ui_scores.sort(key=lambda x: ui_scores[x].value, reverse=True)
    for i in range(len(ui_scores) - 1):
        ui_scores[i].pos[1] = 10 + i * 30


def is_game_end():
    return False


def boardcast_win_player(win_player_idx):
    pass


def end_boardcast():
    GamePlay.restart_game()
