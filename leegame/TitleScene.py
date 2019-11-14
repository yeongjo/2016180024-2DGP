from PicoModule import *
import game_framework
import PlayerReadyChecker as prc

objsList = None

def make_objs():
    ui_mouse = DrawObj()
    ui_mouse.load_img('img/ui_mouse.png')
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
            game_framework.change_state()


def draw():
    for view in View.views:
        view.use()
        objsList.render(view.cam)
        pc.update_canvas()
        pc.clear_canvas()

        render_key_status()
    View.views[0].use()
    render_mouse_status()

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
            if a.key == SDLK_W or a.key == SDLK_A or a.key == SDLK_S or a.key == SDLK_D:
                prc.set_key_input()
