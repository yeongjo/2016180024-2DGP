from PicoModule import *
import game_framework
import copy as cp
import random


EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING = (218, -139, -500)
MAP_WIDTH = 1920
MAP_HEIGHT = 1080
MAP_HALF_WIDTH= MAP_WIDTH // 2
MAP_HALF_HEIGHT = MAP_HEIGHT // 2

objsList = None

ui_hp2, ui_hp1 = None, None

stair_list = []

obj_name_list = ['냉장고', '복사기', '에어컨', '전등', '정수기', '컴터']

# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT if floor >= 3 else EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor]

def restart_game():
    Actor.clear_actors()
    Player2.this.init()

from GameManager import GameManager
from Player2 import Player2
from Stair import Stair
from InteractObj import InteractObj
from Cursor import Cursor
from ActorBrain import ActorBrain
from Actor import Actor
from Building import Building
from UI import Ui
from UiHp import UiPlayer


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
    global buildings
    buildings = []
    building_pos = [[0, MAP_HEIGHT], [MAP_WIDTH - 1, MAP_HEIGHT], [0, 0], [MAP_WIDTH - 1, 0]]
    stair_pos_x = (649, 540)
    i = 0
    
    while i < 4:
        buildings.append(Building())
        buildings[i].pos = np.array(building_pos[i])
        is_right = i % 2
        if is_right == 1:
            buildings[i].imgs[0].filp = True
            buildings[i].imgs[1].filp = True
        for y in EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING:
            stair = Stair()
            stair.set_pos(-stair_pos_x[0] + 18 * is_right + buildings[i].pos[0], y + buildings[i].pos[1])
        for y in EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING:
            stair = Stair()
            stair.set_pos(stair_pos_x[1] + 18 * is_right + buildings[i].pos[0], y + buildings[i].pos[1])
            stair.imgs[1].filp = stair.imgs[0].filp = True
        i += 1

    i = 0
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

    cursor = Cursor()
    cursor.anim.load('img/cursor.png', 1, 1, np.array([0, 0]))
    cursor.anim.load('img/cursor_attack_start.png', 3, 4, np.array([0, 0]))
    cursor.anim.load('img/cursor_attack_doing.png', 1, 2, np.array([0, 0]))
    cursor.anim.load('img/cursor_attack_shot.png', 3, 1, np.array([0, 0]))

    ui_mouse = Ui()
    ui_mouse.load_img('img/ui_mouse.png')
    ui_mouse.set_pos(366, 90)
    ui_mouse.set_off((-1, 0))

    ui_keyboard = Ui()
    ui_keyboard.load_img('img/ui_keyboard.png')
    ui_keyboard.set_pos(-366, 90)
    ui_keyboard.set_off((1, 0))

    global ui_hp1, ui_hp2
    ui_hp1 = UiPlayer()
    ui_hp1.set_pos(-369, 64)
    ui_hp1.size[0], ui_hp1.size[1] = 0, 35
    ui_hp1.init(240, 63, 63, -1.0, ui_keyboard.pos)

    ui_hp2 = UiPlayer()
    ui_hp2.set_pos(369, 64)
    ui_hp2.size[0], ui_hp2.size[1] = 0, 35
    ui_hp2.init(91, 215, 232, 1.0, ui_mouse.pos)

    ui_center = Ui()
    ui_center.load_img('img/ui_center.png')
    ui_center.set_pos(0, 90)



    

is_enter_before = False
# -----------------------------------main code start-----------------------------------

def enter():
    #pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE)  # 마우스 화면밖에 못나가게
    
    pc.SDL_WarpMouseInWindow(View.active_view.window, View.active_view.w // 2, View.active_view.h // 2)
    
    global objsList
    if objsList == None:
        objsList = ObjsList()
    objsList.active()

    global is_enter_before
    if not is_enter_before:
        make_objs()
    else:
        restart_game()

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
    pass

def handle_events():
    events = pc.get_events()
    for a in events:
        if a.type == pc.SDL_QUIT:
            game_framework.exit_game()

        # ESC 게임 종료
        if a.type == pc.SDL_KEYDOWN and a.key == pc.SDLK_ESCAPE:
            game_framework.quit()

        # 마우스 입력
        if a.type == pc.SDL_MOUSEBUTTONDOWN and a.button == 1:
            MouseController.interact_input(True)
        if a.type == pc.SDL_MOUSEMOTION:
            MouseController.mouse_input(a.x, a.y)

        if a.type == pc.SDL_MOUSEBUTTONUP and a.button == 1:
            MouseController.interact_input(False)


        if not GameManager.is_paused:
            # 키보드 입력
            if a.type == pc.SDL_KEYDOWN:
                if a.key == 97:  # a
                    KeyController.x -= 1
                    Player2.this.move_stair(Player2.KEY_A)
                if a.key == 100:  # d
                    KeyController.x += 1
                    Player2.this.move_stair(Player2.KEY_D)
                if a.key == 115:  # s
                    KeyController.interact_input(True)
                    Player2.this.move_stair(Player2.KEY_S)
                if a.key == 119:  # w
                    Player2.this.move_stair(Player2.KEY_W)

                # 카메라 줌 확인용
                if a.key == 61:
                    View.views[0].cam.size += 0.5
                if a.key == 45:
                    View.views[0].cam.size -= 0.5

                


            if a.type == pc.SDL_KEYUP:
                if a.key == 97:  # a
                    KeyController.x += 1
                if a.key == 100:  # d
                    KeyController.x -= 1
                if a.key == 115:  # s
                    KeyController.interact_input(False)

        else:
            Player2.this.is_die = True
