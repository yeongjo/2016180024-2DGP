# Load Image함수에도 랜더러받는게 있어서 개고생했다 ㅠ
from PicoModule import *

firstScene = Scene()
views = [View(0, firstScene), View(1, firstScene)]
player1_controller = Player1Controller()
player2_controller = Player2Controller()
running = True


# 배경그려야함

class Cursor(DrawObj):

    def tick(self, dt):
        global player1_controller
        pos = player1_controller.pos
        speed = 1000
        self.pos = mouse_pos_to_world(player1_controller.pos, views[0])
        t = 1 / views[0].cam.size
        self.pos[0], self.pos[1] = int(self.pos[0] * 1 / views[0].cam.size), int(self.pos[1] * 1 / views[0].cam.size)
        self.pos = self.pos + np.array([self.imgs[0].size[0] / 2, -self.imgs[0].size[1] / 2]) + views[0].cam.pos

        # views[1].cam.pos[0] = 500
        # 리스트 초기화를 클래스 안에서 함수없이 하니까 정적변수처럼되버림
        if dt * speed > 500:
            return
        if pos[0] < 20:
            views[0].cam.pos[0] -= dt * speed
        if pos[0] > views[0].w - 20:
            views[0].cam.pos[0] += dt * speed
        if pos[1] < 20:
            views[0].cam.pos[1] += dt * speed
        if pos[1] > views[0].h - 20:
            views[0].cam.pos[1] -= dt * speed


class Player2(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, views, np.array([80, 0]))
        self.anim.load('img/user_walk.png', 1, 8, views, np.array([80, 0]))
        self.anim.load('img/user_run.png', 1, 4, views, np.array([80, 0]))
        self.pos[1] = -139

    def tick(self, dt):
        global player2_controller
        speed = 300
        run = player2_controller.moveTime.check(dt)
        if player2_controller.x > 0:
            self.anim.flip = 'h'
            if run == 2:
                self.anim.play(2)
                speed *= 1.8
            else:
                self.anim.play(1)
        elif player2_controller.x < 0:
            self.anim.flip = ''
            if run == 2:
                self.anim.play(2)
                speed *= 1.8
            else:
                self.anim.play(1)
        else:
            self.anim.play(0)

        self.pos[0] += player2_controller.x * speed * dt
        self.anim.tick(dt)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)

class Stair(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.load_img('img/stair.png', views)


    def set_pos(self,x,y):
        self.pos = np.array([x+ self.imgs[0].img.w / 2, y + self.imgs[0].img.h / 2])

    # def render(self, cam):
    #     tem_pos, tem_size = self.calculate_pos_size(cam)


class InteractObj(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.anim = Animator()
        self.pos[1] = -139

    def tick(self, dt):
        self.anim.tick(dt)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)


def init():
    pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE)
    img1 = DrawObj(firstScene.objM)
    img1.load_img('img/map.png', views)

    img2 = DrawObj(firstScene.objM)
    img2.load_img('img/a.png', views)
    img2.pos = np.array([200, 200])

    cursor = Cursor(firstScene.objM)
    cursor.load_img('img/cursor.png', views)

    i = 0
    tem_floor = (218,-139,-500)
    t_pos = []
    for y in tem_floor:
        stair = Stair(firstScene.objM)
        stair.set_pos(-649, y)
    for y in tem_floor:
        stair = Stair(firstScene.objM)
        stair.set_pos(540, y)
        stair.imgs[0].filp = True
        stair.imgs[1].filp = True

    player2 = Player2(firstScene.objM)

    t = InteractObj(firstScene.objM)
    t.anim.load('img/냉장고_off.png', 1, 1, views, np.array([0, 0]))

def loop(dt):  # View 각자의 그리기를 불러줌
    # views[0].cam.pos = mouse_pos_to_world(player1_controller.pos,views[0])
    views[0].tick(pc.get_dt())
    views[0].render()
    views[1].render()


def input_handle():
    global running
    events = pc.get_events()
    for a in events:
        if a.type == pc.SDL_QUIT:
            running = False
            print("왜안꺼져")  # 미안..
        if a.type == pc.SDL_MOUSEBUTTONDOWN:
            if (a.button == 1):
                print('down')
        if a.type == pc.SDL_MOUSEMOTION:
            player1_controller.mouseInput(a.x, a.y)

        if a.type == pc.SDL_MOUSEBUTTONUP:
            if (a.button == 1):
                print('left mouse up')
        if a.type == pc.SDL_KEYDOWN:

            if a.key == 97:  # a
                player2_controller.x -= 1
            if a.key == 100:  # d
                player2_controller.x += 1
            if a.key == 115:  # s
                player2_controller.interact_input(True)
            if a.key == 27:
                running = False
            if a.key == 61:
                views[0].cam.size += 0.5
            if a.key == 45:
                views[0].cam.size -= 0.5

        if a.type == pc.SDL_KEYUP:
            print(a.key)
            if a.key == 97:  # a
                player2_controller.x += 1
            if a.key == 100:  # d
                player2_controller.x -= 1
            if a.key == 115:  # s
                print("hi")
                player2_controller.interact_input(False)


init()

while running:
    input_handle()
    loop(pc.dt)
