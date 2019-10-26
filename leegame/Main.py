# Load Image함수에도 랜더러받는게 있어서 개고생했다 ㅠ
from PicoModule import *
import copy as cp
import random

firstScene = Scene()
views = [View(0, firstScene), View(1, firstScene)]
player1_controller = Player1Controller()
player2_controller = Player2Controller()

running = True
floor_height = (218, -139, -500)
map_size = (1920, 1080)

init_text()


# 배경그려야함

class Cursor(DrawObj):

    def tick(self, dt):
        global player1_controller
        pos = player1_controller.pos
        speed = 1000
        self.pos = mouse_pos_to_world(pos, views[0]) + np.array([self.imgs[0].size[0] / 2, -self.imgs[0].size[1] / 2])

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

        if player1_controller.clickTime.check(dt) == 1:
            interact_to_obj(1)

    def render(self, cam):
        tem_pos, tem_size = super().render(cam)
        debug_text(str(self.pos + np.array([-self.imgs[0].img.w // 2, self.imgs[0].img.h // 2])), tem_pos)


interact_obj_list = []


def add_interact_obj(interact_obj):
    interact_obj_list.append(interact_obj)


def interact_to_obj(player_idx):
    small_len_obj = None
    small_len = 300000000
    for a in interact_obj_list:
        if player_idx == 1:
            _pos = mouse_pos_to_world(player1_controller.pos, views[0])
            _pos[1] -= 150
        elif player_idx == 2:
            _pos = player2.pos
        _vec = _pos - a.get_floor_pos()
        _len = sum(x * x for x in _vec)
        if _len < small_len:
            small_len = _len
            small_len_obj = a

    if small_len_obj is not None:
        small_len_obj.interact_input(player_idx, small_len)


class Player2(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.load_img('img/stair_move.png', views)
        self.size[0], self.size[1] = 1, 1
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, views, np.array([80, 0]))
        self.anim.load('img/user_walk.png', 1, 8, views, np.array([80, 0]))
        self.anim.load('img/user_run.png', 1, 4, views, np.array([80, 0]))
        self.anim.load('img/user_active.png', 3, 3, views, np.array([80, 0]))  # 3
        self.pos[1] = floor_height[1]
        self.interact_obj = None  # 있을 때 움직이면 인터렉트 오브젝트 비활성화 용
        self.is_in_stair = False


        hw = views[1].w // 2
        hh = views[1].h // 2
        views[1].cam.pos = self.pos - np.array([hw, hh - 200])

    def tick(self, dt):
        global player2_controller
        self.update_camera(dt)
        if self.is_in_stair:
            return
        speed = 300
        run = player2_controller.moveTime.check(dt)
        if run == 1:
            # 인터렉트
            self.anim.play(3, 0)
        else:
            if player2_controller.x > 0:
                if self.interact_obj != None:
                    self.interact_obj.cancel_by_move()
                self.anim.flip = 'h'
                if run == 2:
                    self.anim.play(2)
                    speed *= 1.8
                else:
                    self.anim.play(1)
            elif player2_controller.x < 0:
                if self.interact_obj != None:
                    self.interact_obj.cancel_by_move()
                self.anim.flip = ''
                if run == 2:
                    self.anim.play(2)
                    speed *= 1.8
                else:
                    self.anim.play(1)
            else:
                if self.anim.isEnd:
                    self.anim.play(0)

        self.pos[0] += player2_controller.x * speed * dt
        end_anim_idx = self.anim.tick(dt)
        if end_anim_idx == 3:
            interact_to_obj(2)

        self.check_stair()

    #tick 에서 불림 계단이랑 부딫히면 계단안에 들어간 상태로 변경
    def check_stair(self):
        if self.is_in_stair:
            return
        i = 0
        t_count = len(stair_list)
        while i < t_count:
            if stair_list[i].check_player_pos(self.pos):
                self.is_in_stair = True
                print("check_stair : true", stair_list[i].pos, self.pos)
                return
            i += 1

    #계단 안에서 움직이기
    def move_stair(self, input_key):
        if not self.is_in_stair:
            return
        i = 0
        t_count = len(stair_list)
        while i < t_count:
            if stair_list[i].check_player_pos(self.pos):
                stair_list[i].send_player(input_key, i)
                return
            i += 1

    def update_camera(self, dt):
        hw = views[1].w // 2
        hh = views[1].h // 2
        player_pos = self.pos - np.array([hw, hh - 200])
        views[1].cam.pos += (player_pos - views[1].cam.pos) * dt * 3

    def render(self, cam):
        if self.interact_obj != None:
            return
        tem_pos, tem_size = self.calculate_pos_size(cam)
        if self.is_in_stair:
            if cam.idx == 1:
                tem_pos[1] += 150
                self.imgs[1].render(tem_pos, tem_size)
            return
        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.pos), tem_pos)


class Building(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.load_img('img/map.png', views)


stair_list = []


class Stair(DrawObj):

    # 중간 계단은 계단이 두개인데 서로 참조하고있어야 플레이어가 넘어갈수있게 만들어줄수있다.

    def __init__(self, objm):
        super().__init__(objm)
        self.load_img('img/stair.png', views)
        self.otherStair = None
        stair_list.append(self)

    def set_pos(self, x, y):
        self.pos = np.array([x + self.imgs[0].img.w / 2, y + self.imgs[0].img.h / 2])

    def check_player_pos(self, pos):
        _pos = self.pos - pos
        _len = sum(x * x for x in _pos)
        if _len < 15000:
            return True
        return False

    #플레이어를 딴곳으로 보내줌
    def send_player(self, input_idx, my_idx):  # input_idx 0:w 1:a 2:s 3:d
        print(input_idx)
        if input_idx == 0:
            if my_idx % 3 == 0 and my_idx < 12:
                return
            if my_idx >= 12 and my_idx % 3 == 0:
                player2.pos = cp.copy(stair_list[my_idx - 10].pos)
            else:
                player2.pos = cp.copy(stair_list[my_idx - 1].pos)
        elif input_idx == 2:
            if my_idx % 3 == 2 and my_idx >= 12:
                return
            if my_idx < 12 and my_idx % 3 == 2:
                player2.pos = cp.copy(stair_list[my_idx + 10].pos)
            else:
                player2.pos = cp.copy(stair_list[my_idx + 1].pos)

        elif input_idx == 1:
            if 6 <= my_idx <= 8 or 6 + 12 <= my_idx <= 8 + 12:  # 옆방으로
                player2.pos = cp.copy(stair_list[my_idx - 3].pos)
            else:
                player2.pos = cp.copy(self.pos)
                if 0 <= my_idx <= 2 or 0 + 12 <= my_idx <= 2 + 12:
                    pass
                else:
                    player2.pos[0] -= 150
                player2.is_in_stair = False
        elif input_idx == 3:
            if 3 <= my_idx <= 5 or 3 + 12 <= my_idx <= 5 + 12:  # 옆방으로
                player2.pos = cp.copy(stair_list[my_idx + 3].pos)
            else:
                player2.pos = cp.copy(self.pos)
                if 9 <= my_idx <= 11 or 9 + 12 <= my_idx <= 11 + 12:
                    pass
                else:
                    player2.pos[0] += 150
                player2.is_in_stair = False
        player2.pos[1] -= 95


class InteractObj(DrawObj):
    # doing_limit_time이 0 이상이면 키는 시간이 존재함
    def __init__(self, objm, doing_limit_time=-1):
        super().__init__(objm)
        self.anim = Animator()
        #self.pos[1] = -139
        self.doing_remain_time = 0
        self.floor_y = None
        self.doing_limit_time = doing_limit_time  # 0 이상이면 키는 시간이 존재함
        self.is_playing_doing = False # 플레이어가 키는시간이 있고 그 키는 시간중임을 표시
        add_interact_obj(self)

    def tick(self, dt):
        self.anim.tick(dt)
        if self.is_playing_doing:
            self.doing_remain_time += dt
            if self.doing_limit_time < self.doing_remain_time:
                self.is_playing_doing = False
                self.anim.play(1)
                global player2
                player2.interact_obj = None
                print("player2 interact! : on tick")

    def cancel_by_move(self):
        if self.is_playing_doing == False:
            return
        self.is_playing_doing = False
        global player2
        player2.interact_obj = None
        self.interact(1)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.pos), tem_pos)
        debug_text(str(self.floor_y), tem_pos + np.array([0,20]))

    def interact(self, player_idx, is_interacting=False):
        if player_idx == 1:
            self.anim.play(0)
        elif player_idx == 2:
            if self.doing_limit_time >= 0:
                self.anim.play(2)
                self.doing_remain_time = 0
                self.is_playing_doing = True
                global player2
                player2.interact_obj = self
                print("player2 interact! : is_has_doing")
            else:
                self.anim.play(1)
                print("player2 interact!")
            # else:
            #     self.anim.play(2)
            #     print('player2 interacting')
    
    # 이 오브젝트의 바닥위치 구하기
    def get_floor_pos(self):
        if self.floor_y is None:
            floor_offset = 0
            if self.pos[1] > map_size[1]//2:
                t_pos_y = self.pos[1] - map_size[1]
                floor_offset = map_size[1]
            else:
                t_pos_y = self.pos[1]
            #self.floor_y = floor_height[0]
            for t in floor_height:
                self.floor_y = t + floor_offset
                if t <= t_pos_y:
                    break

        return np.array([self.pos[0], self.floor_y])

    def interact_input(self, player_idx, small_len):
        assert player_idx != 0, "player_idx != 0"
        if small_len < 150*150:
            print("interect with obj")
            self.interact(player_idx)


# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return floor_height[floor % 3] + map_size[1] if floor >= 3 else floor_height[floor]


# 층은 0층부터 시작
def make_obj(name, x, floor):
    t = InteractObj(firstScene.objM)
    t.pos[0] = x
    t.pos[1] = calculate_floor_height(floor)
    if name == '에어컨':
        t.pos[1] += 100
    t.anim.load('img/' + name + '_off.png', 1, 1, views, np.array([0, 0]))
    if name == '복사기':
        t.anim.load('img/복사기_on.png', 1, 4, views, np.array([0, 0]))
        t.anim.load('img/복사기_start.png', 1, 2, views, np.array([0, 0]))
    else:
        t.anim.load('img/' + name + '_on.png', 1, 2, views, np.array([0, 0]))
    return t


obj_name_list = ['냉장고', '복사기', '에어컨', '전등', '정수기', '컴터']


def make_random_floor_obj(x, floor):
    wall_size = 400
    offset =  x*map_size[0] - map_size[0]//2
    i = wall_size + offset
    limit_x = map_size[0] - wall_size + offset
    while i < limit_x - 300:
        random_x = i
        obj = make_obj(obj_name_list[random.randint(0, len(obj_name_list) - 1)],
                 random_x, floor)
        obj_size_w = obj.anim.animArr[0].size[0]
        obj_size_hw = obj_size_w // 2
        obj.pos[0] += obj_size_hw
        i += obj_size_w + random.randint(0, 200)


class Ui(DrawObj):
    def render(self, cam):
        vw = views[cam.idx].w // 2
        vh = views[cam.idx].h
        ratio1 = views[cam.idx].w / map_size[0]
        #h = views[cam.idx].h / map_size[1]
        tem_size = np.array([ratio1,ratio1])
        tem_pos = np.array([(self.pos[0] - map_size[0] // 2)*ratio1 + vw , vh -self.pos[1]*ratio1])
        tem_size *= 1.3
        self.imgs[cam.idx].render(tem_pos, tem_size)


def init():
    # pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE) # 마우스 화면밖에 못나가게
    pc.SDL_WarpMouseInWindow(views[0].window, views[0].w // 2, views[0].h // 2)

    global buildings
    buildings = []
    building_pos = [[0, map_size[1]], [map_size[0]-1, map_size[1]], [0, 0], [map_size[0]-1, 0]]
    stair_pos_x = (649, 540)
    i = 0
    while i < 4:
        buildings.append(Building(firstScene.objM))
        buildings[i].pos = np.array(building_pos[i])
        is_right = i % 2
        if is_right == 1:
            buildings[i].imgs[0].filp = True
            buildings[i].imgs[1].filp = True
        for y in floor_height:
            stair = Stair(firstScene.objM)
            stair.set_pos(-stair_pos_x[0]+18*is_right + buildings[i].pos[0], y + buildings[i].pos[1])
        for y in floor_height:
            stair = Stair(firstScene.objM)
            stair.set_pos(stair_pos_x[1]+18*is_right + buildings[i].pos[0], y + buildings[i].pos[1])
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

    global player2
    player2 = Player2(firstScene.objM)

    cursor = Cursor(firstScene.objM)
    cursor.load_img('img/cursor.png', views)

    ui_center = Ui(firstScene.objM)
    ui_center.load_img('img/ui_center.png', views)

    ui_mouse = Ui(firstScene.objM)
    ui_mouse.load_img('img/ui_mouse.png', views)
    ui_mouse.set_pos(266, 100)


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
                player1_controller.interact_input(True)
        if a.type == pc.SDL_MOUSEMOTION:
            player1_controller.mouseInput(a.x, a.y)

        if a.type == pc.SDL_MOUSEBUTTONUP:
            if (a.button == 1):
                player1_controller.interact_input(False)

        if a.type == pc.SDL_KEYDOWN:

            if a.key == 97:  # a
                player2_controller.x -= 1
                player2.move_stair(1)
            if a.key == 100:  # d
                player2_controller.x += 1
                player2.move_stair(3)
            if a.key == 115:  # s
                player2_controller.interact_input(True)
                player2.move_stair(2)
            if a.key == 119:  # w
                player2.move_stair(0)
            if a.key == 27:
                running = False
            if a.key == 61:
                views[0].cam.size += 0.5
            if a.key == 45:
                views[0].cam.size -= 0.5

        if a.type == pc.SDL_KEYUP:
            print("key up: ", a.key)
            if a.key == 97:  # a
                player2_controller.x += 1
            if a.key == 100:  # d
                player2_controller.x -= 1
            if a.key == 115:  # s
                # print("hi")
                player2_controller.interact_input(False)


init()

while running:
    input_handle()
    loop(pc.dt)
