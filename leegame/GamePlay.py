from PicoModule import *
import game_framework
import random
from ctypes import *
import GameManager
from Player import Player
from InteractObj import InteractObj
from ActorBrain import ActorBrain
from Actor import Actor
from Building import *
import NetworkManager

bgm = None


# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT if floor >= 3 else \
        EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor]


def restart_game():
    Actor.clear_actors()
    # random_actor_generator()
    for a in View.views:
        a.cam.reset_size()


# 층은 0층부터 시작
def make_furniture(x, y):
    t = InteractObj()
    t.pos[0] = x
    t.pos[1] = y
    t.size[0] = 50
    t.size[1] = 100
    return t


def make_random_floor_obj(x, floor):
    wall_size = 400
    offset = x * MAP_WIDTH - MAP_HALF_WIDTH
    i = wall_size + offset
    limit_x = MAP_WIDTH - wall_size + offset
    while i < limit_x - 300:
        random_x = i
        obj = make_furniture(random_x, calculate_floor_height(floor))
        obj_size_w = obj.size[0]
        obj_size_hw = obj_size_w // 2
        obj.pos[0] += obj_size_hw
        i += obj_size_w + random.randint(100, 400)


def make_furniture_by_packet(packet):
    for i in range(len(packet)-1):
        make_furniture(packet[i][0], packet[i][1])


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


def make_objs(objs_pos):
    Building.create_buildings()

    # Make Obj
    # for j in range(2):
    #     for i in range(6):
    #         make_random_floor_obj(j, i)

    # random_actor_generator()
    for pos in objs_pos:
        make_furniture(pos[0], pos[1])


objM = None


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
        objM.active()

    make_objs()

    GameManager.init()


def update(dt):  # View 각자의 그리기를 불러줌
    objM.tick(dt)


def draw():
    for view in View.views:
        view.use()
        objM.render(view.cam)
        pc.update_canvas()
        pc.clear_canvas()


def exit():
    bgm.stop()


KEY_A = 97
KEY_D = 100
KEY_S = 115
KEY_W = 119
KEY_H = 104
KEY_J = 106
KEY_K = 107

clientKeyInputPacket = NetworkManager.ClientKeyInputPacket()


def handle_events():
    events = pc.get_events()
    mouse_pos_x, mouse_pos_y = c_int(), c_int()
    pc.SDL_GetMouseState(mouse_pos_x, mouse_pos_y)
    for a in events:
        if a.type == pc.SDL_QUIT:
            game_framework.quit()

        # 키보드 입력
        if a.type == pc.SDL_KEYDOWN:
            clientKeyInputPacket.key = a.key
            if a.key in [KEY_A, KEY_D, KEY_S, KEY_W, KEY_H, KEY_J, KEY_K]:
                clientKeyInputPacket.isDown = True
                NetworkManager.SendClientKeyInputPacketToServer(clientKeyInputPacket)

            # ESC 게임 종료
            if a.key == pc.SDLK_ESCAPE:
                import TitleScene
                game_framework.change_state(TitleScene)

        if a.type == pc.SDL_KEYUP:
            if a.key in [KEY_A, KEY_D, KEY_J]:
                clientKeyInputPacket.isDown = False
                NetworkManager.SendClientKeyInputPacketToServer(clientKeyInputPacket)
