from PicoModule import *
import game_framework
import PlayerReadyChecker as prc
import GamePlay as NextScene
from Button import Button
import random

objM = None
bgm = None

is_first = False
ready_time = 1
ready_remain_time = 1


def game_start():
    prc.keyuser_ready = True


def set_window_size_1920():
    change_view_size(1920, 1080)


def set_window_size_1280():
    change_view_size(1280, 720)

def set_window_size_720():
    change_view_size(720, 405)


def make_objs():
    ui_mouse = DrawObj()
    ui_mouse.load_img('img/Title.png')
    ui_mouse.pos = np.array(ui_mouse.get_halfsize())

    Button(10, 10, 200, 100, "1920", set_window_size_1920)
    Button(10, 110, 200, 200, "1280", set_window_size_1280)
    Button(10, 210, 200, 300, "720", set_window_size_720)


# 타이틀 신 들와서 처음 시작
def enter():
    set_window_size_1280()
    random.seed(9000)
    pc.SDL_SetRelativeMouseMode(pc.SDL_FALSE)  # 마우스 화면밖에 못나가게
    KeyController.x = 0

    global bgm
    if (bgm == None):
        bgm = pc.load_music('sound/Title.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    View.reset()
    global objM
    if objM == None:
        objM = ObjM()
    objM.active()

    global is_first
    if not is_first:
        make_objs()

    prc.reset()

    import NetworkManager
    NetworkManager.StartClientSocket()

    is_enter_before = True


def update(dt):  # View 각자의 그리기를 불러줌
    objM.tick(dt)

    if prc.check_ready_status():
        global ready_remain_time
        ready_remain_time -= dt
        if ready_remain_time <= 0:
            ready_remain_time = -1
            game_framework.change_state(NextScene)


def draw():
    i = 0
    for view in View.views:
        pc.update_canvas()
        pc.clear_canvas()
        view.use()
        objM.render(view.cam)

        text_pos = get_center()
        text_pos[0] -= 300
        text_pos[1] -= 300
        prc.render_status(i, text_pos)

        i += 1


def exit():
    bgm.stop()


def handle_events():
    events = pc.get_events()
    for a in events:
        if a.type == pc.SDL_QUIT:
            game_framework.quit()

        # ESC 게임 종료
        if a.type == pc.SDL_KEYDOWN and a.key == pc.SDLK_ESCAPE:
            game_framework.quit()

        # 마우스 입력
        if a.type == pc.SDL_MOUSEBUTTONDOWN and a.button == 1:
            prc.set_mouse_input()
            MouseController.is_down = True
        elif a.type == pc.SDL_MOUSEBUTTONUP and a.button == 1:
            MouseController.is_down = False
        #
        # if a.type == pc.SDL_KEYDOWN:
        #     if a.key == 97:  # a
        #         KeyController.x -= 1
        #     if a.key == 100:  # d
        #         KeyController.x += 1
        #
        # if a.type == pc.SDL_KEYUP:
        #     if a.key == 97:  # a
        #         KeyController.x += 1
        #     if a.key == 100:  # d
        #         KeyController.x -= 1
        #
        if a.type == pc.SDL_MOUSEMOTION:
            MouseController.mouse_input(a.x, a.y)
        #
        # if a.type == pc.SDL_KEYDOWN:
        #     if a.key == 97 or a.key == 100 or a.key == 115 or a.key == 119:
        #         prc.set_key_input()
