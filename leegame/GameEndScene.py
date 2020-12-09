from PicoModule import *
import game_framework
import PlayerReadyChecker as prc
import TitleScene as NextScene
import GameManager

objM = None

background = None
victory_img = None
bgm = None

def make_objs():
    global victory_img, background
    background = DrawObj()

    if GameManager.is_local_player_win():
        background.load_img("img/1_win.png")
        # victory_img.imgs =
    # if GameManager.get_winning_player_idx() == GameManager.MOUSEUSER:
    #     background.load_img("img/leewin.png")
    # else:
    #     background.load_img("img/enemywin.png")

    # if GameManager.mouseuser_ui is not None:
    #     victory_img = DrawObj()
    #     if GameManager.get_winning_player_idx() == GameManager.MOUSEUSER:
    #         victory_img.imgs = GameManager.mouseuser_ui.imgs
    #     else:
    #         victory_img.imgs = GameManager.keyuser_ui.imgs
    
    else:
        background.load_img("img/2_Lose.png")
    background.pos = np.array(background.get_halfsize())

is_first = False
is_ready_all = False
ready_time = 1
ready_remain_time = 3
objM = None

def enter():
    pc.SDL_SetRelativeMouseMode(pc.SDL_FALSE)  # 마우스 화면밖에 못나가게

    # global bgm
    # if (bgm == None):
    #     bgm = pc.load_music('sound/Win.mp3')
    # bgm.set_volume(64)
    # bgm.play()

    View.reset()

    global objM
    if objM == None:
        objM = ObjM()
    objM.active()


    ready_remain_time = ready_time

    make_objs()

    # if victory_img is not None:
    #     victory_img.pos[0] = 1920//2
    #     victory_img.pos[1] = 1080 - victory_img.get_halfsize()[1] + 100

    prc.reset()
    prc.keyuser_ready = True
    is_enter_before = True


def update(dt):  # View 각자의 그리기를 불러줌
    # objM.tick(dt)

    if prc.check_ready_status():
        global ready_remain_time
        ready_remain_time -= dt
        if ready_remain_time <= 0:
            ready_remain_time = -1
            game_framework.quit()
            # game_framework.change_state(NextScene)


def draw():
    i = 0
    for view in View.views:
        pc.update_canvas()
        pc.clear_canvas()
        view.use()
        objM.render(view.cam)

        text_pos = get_center()
        text_pos[1] -= 300
        # prc.render_status(i, text_pos)

        i += 1

def exit():
    # bgm.stop()
    objM.clear()

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
