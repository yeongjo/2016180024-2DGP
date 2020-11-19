from PicoModule import *
import game_framework
import random
from ctypes import *

EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING = (218, -139, -500)
MAP_WIDTH = 1920
MAP_HEIGHT = 1080
MAP_HALF_WIDTH = MAP_WIDTH // 2
MAP_HALF_HEIGHT = MAP_HEIGHT // 2

stair_list = []
ui_scores = []
playerCnt = 0

bgm = None


# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT if floor >= 3 else \
        EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor]


def restart_game():
    if not is_first: return
    Actor.clear_actors()
    random_actor_generator()
    Player.this.init()
    for a in View.views:
        a.cam.reset_size()
    InteractObj.reset_all()


import GameManager
from Player import Player
from InteractObj import InteractObj
from ActorBrain import ActorBrain
from Actor import Actor
from Building import Building
from UiScore import UiScore


# 층은 0층부터 시작
def make_obj(x, floor):
    t = InteractObj()
    t.pos[0] = x
    t.pos[1] = calculate_floor_height(floor)
    return t


def make_random_floor_obj(x, floor):
    wall_size = 400
    offset = x * MAP_WIDTH - MAP_HALF_WIDTH
    i = wall_size + offset
    limit_x = MAP_WIDTH - wall_size + offset
    while i < limit_x - 300:
        random_x = i
        obj = make_obj(random_x, floor)
        obj_size_w = obj.size
        obj_size_hw = obj_size_w // 2
        obj.pos[0] += obj_size_hw
        i += obj_size_w + random.randint(0, 200)


def random_actor_generator():
    for j in range(2):
        x = j * MAP_WIDTH
        for i in range(6):
            for k in range(random.randint(0, 3)):
                brain_way_off = MAP_HALF_WIDTH - 500
                actor = Actor()
                actor.pos[0] = random.uniform(x - brain_way_off, x + brain_way_off)
                actor.pos[1] = calculate_floor_height(i)
                brain = ActorBrain(actor, (x - brain_way_off, x + brain_way_off))
                actor.set_brain(brain)


def make_objs():
    Building.create_buildings()
    # 계단끼리 연결
    for i in range(3):
        stair_list[i + 3].other_stair = stair_list[i + 6]
        stair_list[i + 6].other_stair = stair_list[i + 3]
        stair_list[i + 3 + 12].other_stair = stair_list[i + 6 + 12]
        stair_list[i + 6 + 12].other_stair = stair_list[i + 3 + 12]

    # Make Obj
    for j in range(2):
        for i in range(6):
            make_random_floor_obj(j, i)

    random_actor_generator()
    Player()

    # ui ----------------------------
    global ui_scores
    ui_scores.append(UiScore())
    ui_scores[len(ui_scores)-1].set_pos(-369, 64)


is_first = True
my_player_id = -1


# -----------------------------------main code start-----------------------------------

def enter():
    # pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE)  # 마우스 화면밖에 못나가게
    # pc.SDL_WarpMouseInWindow(View.views[0].window, View.views[0].w // 2, View.views[0].h // 2)

    global bgm
    if bgm == None:
        bgm = pc.load_music('sound/MainMusic.mp3')
        bgm.set_volume(64)
    bgm.repeat_play()

    global objM
    if objM is None:
        objM = ObjM()

    global is_first
    if is_first:
        make_objs()
        is_first = False

    GameManager.init()



def update(dt):  # View 각자의 그리기를 불러줌
    GameManager.update(dt)
    objM.tick(dt)


def draw():
    for view in View.views:
        view.use()
        objM.render(view.cam)
        pc.update_canvas()
        pc.clear_canvas()


def exit():
    bgm.stop()


def handle_events():
    events = pc.get_events()
    mouse_pos_x, mouse_pos_y = c_int(), c_int()
    pc.SDL_GetMouseState(mouse_pos_x, mouse_pos_y)
    for a in events:
        if a.type == pc.SDL_QUIT:
            game_framework.quit()

        # 키보드 입력
        if a.type == pc.SDL_KEYDOWN:
            print(a.key)
            if a.key == 97:  # a
                KeyController.x -= 1
                if KeyController.x < -1:
                    KeyController.x = -1
                Player.move_stair(Player.KEY_A)
            if a.key == 100:  # d
                KeyController.x += 1
                if KeyController.x > 1:
                    KeyController.x = 1
                Player.move_stair(Player.KEY_D)
            if a.key == 115:  # s
                KeyController.interact_input(True)
                Player.move_stair(Player.KEY_S)
            if a.key == 119:  # w
                Player.move_stair(Player.KEY_W)

            # 카메라 줌 확인용
            if a.key == 61:
                # View.views[0].cam.size += 0.5
                Player.is_die = True
            if a.key == 45:
                # View.views[0].cam.size -= 0.5
                GameManager.boardcast_win_player(GameManager.KEYUSER)

            # ESC 게임 종료
            if a.key == pc.SDLK_ESCAPE:
                import TitleScene
                game_framework.change_state(TitleScene)

        if a.type == pc.SDL_KEYUP:
            if a.key == 97:  # a
                KeyController.x += 1
            if a.key == 100:  # d
                KeyController.x -= 1
            if a.key == 115:  # s
                KeyController.interact_input(False)

