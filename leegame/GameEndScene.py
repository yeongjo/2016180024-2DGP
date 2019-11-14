from PicoModule import *
import game_framework

objsList = None

def make_objs():
    ui_mouse = DrawObj()
    ui_mouse.load_img('img/ui_mouse.png')
    ui_mouse.pos = np.array(get_center())

is_enter_before = False

def enter():
    global objsList
    if objsList == None:
        objsList = ObjsList()
    objsList.active()

    global is_enter_before
    if not is_enter_before:
        make_objs()

    is_enter_before = True


def update(dt):  # View 각자의 그리기를 불러줌
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
            game_framework.quit()

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