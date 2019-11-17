from PicoModule import *
import game_framework
import PlayerReadyChecker as prc
import GamePlay as NextScene

objsList = None

def make_objs():
    ui_mouse = DrawObj()
    ui_mouse.load_img('img/Title.png')
    ui_mouse.pos = np.array(get_center())

is_enter_before = False
is_ready_all = False
ready_time = 1
ready_remain_time = 1

def enter():
    global objsList
    if objsList == None:
        objsList = ObjsList()
    objsList.active()

    ready_remain_time = ready_time

    global is_enter_before
    if not is_enter_before:
        make_objs()

    prc.reset()

    is_enter_before = True


def update(dt):  # View 각자의 그리기를 불러줌
    objsList.tick(dt)

    if prc.check_ready_status():
        global ready_remain_time
        ready_remain_time -= dt
        if ready_remain_time <= 0:
            ready_remain_time = -1;
            game_framework.change_state(NextScene)


def draw():
    i = 0
    for view in View.views:
        pc.update_canvas()
        pc.clear_canvas()
        view.use()
        objsList.render(view.cam)

        text_pos = get_center()
        text_pos[0] -= 300
        text_pos[1] -= 300
        prc.render_status(i, text_pos)

        i += 1

def exit():
    pass

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

        if a.type == pc.SDL_KEYDOWN:
            if a.key == 97 or a.key == 100 or a.key == 115 or a.key == 119:
                prc.set_key_input()
