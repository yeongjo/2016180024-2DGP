from PicoModule import *
import game_framework
import copy as cp
import random
from ctypes import *

EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING = (218, -139, -500)
MAP_WIDTH = 1920
MAP_HEIGHT = 1080
MAP_HALF_WIDTH = MAP_WIDTH // 2
MAP_HALF_HEIGHT = MAP_HEIGHT // 2

objsList = None

ui_hp2, ui_hp1 = None, None

stair_list = []

obj_name_list = ['냉장고', '복사기', '에어컨', '전등', '정수기', '컴터']
bgm = None


# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT if floor >= 3 else \
    EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor]


def restart_game():
    if not is_enter_before: return
    Actor.clear_actors()
    random_actor_generator()
    Player2.this.init()
    for a in View.views:
        a.cam.reset_size()
    InteractObj.reset_all()

from GameManager import GameManager
from Player2 import Player2
from Stair import Stair
from InteractObj import InteractObj
from Cursor import Cursor
from ActorBrain import ActorBrain
from Actor import Actor
from Building import Building
from UI import Ui
from UiHp import PlayerUI


# 층은 0층부터 시작
def make_obj(name, x, floor):
    t = InteractObj()
    t.pos[0] = x
    t.pos[1] = calculate_floor_height(floor)
    if name == '에어컨':
        t.pos[1] += 100
    t.anim.load('img/' + name + '_off.png', 1, 1, np.array([0, 0]))
    if name == '복사기':
        t.anim.load('img/복사기_on.png', 1, 4, np.array([0, 0]))
        t.anim.load('img/복사기_start.png', 1, 2, np.array([0, 0]))
        t.doing_limit_time = 1.0
        t.damage *= 3
    else:
        t.anim.load('img/' + name + '_on.png', 1, 2, np.array([0, 0]))
    return t


def make_random_floor_obj(x, floor):
    wall_size = 400
    offset = x * MAP_WIDTH - MAP_HALF_WIDTH
    i = wall_size + offset
    limit_x = MAP_WIDTH - wall_size + offset
    while i < limit_x - 300:
        random_x = i
        obj = make_obj(obj_name_list[random.randint(0, len(obj_name_list) - 1)],
                       random_x, floor)
        obj_size_w = obj.anim.anim_arr[0].img_width
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

    i = 0
    # 계단끼리 연결
    while i < 3:
        stair_list[i + 3].other_stair = stair_list[i + 6]
        stair_list[i + 6].other_stair = stair_list[i + 3]
        stair_list[i + 3 + 12].other_stair = stair_list[i + 6 + 12]
        stair_list[i + 6 + 12].other_stair = stair_list[i + 3 + 12]
        i += 1

    # Make Obj
    for j in range(2):
        for i in range(6):
            make_random_floor_obj(j, i)

    random_actor_generator()
    Player2()

    # ui ----------------------------

    ui_mouse = Ui((255,50,50))
    ui_mouse.load_img('img/ui_mouse.png')
    ui_mouse.set_pos(0, 90)
    ui_mouse.set_off((-1, 0))

    global ui_hp1, ui_hp2
    ui_hp1 = PlayerUI(1)
    ui_hp1.set_pos(-369, 64)
    ui_hp1.size[0], ui_hp1.size[1] = 0, 35
    ui_hp1.init(240, 63, 63, -1.0, ui_keyboard.pos)

    ui_hp2 = PlayerUI(1)
    ui_hp2.set_pos(369, 64)
    ui_hp2.size[0], ui_hp2.size[1] = 0, 35
    ui_hp2.init(91, 215, 232, 1.0, ui_mouse.pos)


is_enter_before = False
my_player_id = -1

# -----------------------------------main code start-----------------------------------

def enter():
    pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE)  # 마우스 화면밖에 못나가게

    pc.SDL_WarpMouseInWindow(View.views[0].window, View.views[0].w // 2, View.views[0].h // 2)

    global bgm
    if(bgm == None):
        bgm = pc.load_music('sound/MainMusic.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    global objsList
    if objsList == None:
        objsList = ObjsList()
    objsList.active()

    global is_enter_before
    if not is_enter_before:
        make_objs()

    GameManager.init((ui_hp2, ui_hp1))

    is_enter_before = True


def update(dt):  # View 각자의 그리기를 불러줌
    GameManager.update(dt)
    objsList.tick(dt)


def draw():
    for view in View.views:
        view.use()
        objsList.render(view.cam)
        pc.update_canvas()
        pc.clear_canvas()


def exit():
    is_enter_before = False
    bgm.stop()


def handle_events():
    events = pc.get_events()
    import TitleScene
    if TitleScene.isServer:
        mouse_pos_x, mouse_pos_y =  c_int(),c_int()
        pc.SDL_GetMouseState(mouse_pos_x, mouse_pos_y)
        MouseController.mouse_input(int(mouse_pos_x.value), int(mouse_pos_y.value))
    for a in events:
        if a.type == pc.SDL_QUIT:
            game_framework.quit()

        # ESC 게임 종료
        if a.type == pc.SDL_KEYDOWN and a.key == pc.SDLK_ESCAPE:
            import TitleScene
            game_framework.change_state(TitleScene)

        if TitleScene.isServer:
            # 마우스 입력
            if a.type == pc.SDL_MOUSEBUTTONDOWN and a.button == 1:
                MouseController.interact_input(True)
            #if a.type == pc.SDL_MOUSEMOTION:
            #    MouseController.mouse_input(a.x, a.y)

            if a.type == pc.SDL_MOUSEBUTTONUP and a.button == 1:
                MouseController.interact_input(False)
        else:
            # 키보드 입력
            if a.type == pc.SDL_KEYDOWN:
                # print(a.key)
                if a.key == 97:  # a
                    KeyController.x -= 1
                    if KeyController.x < -1:
                        KeyController.x = -1
                    Player2.this.move_stair(Player2.KEY_A)
                if a.key == 100:  # d
                    KeyController.x += 1
                    if KeyController.x > 1:
                        KeyController.x = 1
                    Player2.this.move_stair(Player2.KEY_D)
                if a.key == 115:  # s
                    KeyController.interact_input(True)
                    Player2.this.move_stair(Player2.KEY_S)
                if a.key == 119:  # w
                    Player2.this.move_stair(Player2.KEY_W)

                # 카메라 줌 확인용
                if a.key == 61:
                    # View.views[0].cam.size += 0.5
                    Player2.this.is_die = True
                if a.key == 45:
                    #View.views[0].cam.size -= 0.5
                    GameManager.game_end(GameManager.KEYUSER)

            if a.type == pc.SDL_KEYUP:
                if a.key == 97:  # a
                    KeyController.x += 1
                if a.key == 100:  # d
                    KeyController.x -= 1
                if a.key == 115:  # s
                    KeyController.interact_input(False)

        if GameManager.is_paused:
            Player2.this.is_paused = True
