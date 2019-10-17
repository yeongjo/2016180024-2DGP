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


# 배경그려야함

class Cursor(DrawObj):

    def tick(self, dt):
        global player1_controller
        pos = player1_controller.pos
        speed = 1000
        self.pos = mouse_pos_to_view_pos(player1_controller.pos, views[0])
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

        if player1_controller.clickTime.check(dt) == 1:
            interact_to_obj(1)


interact_obj_list = []


def add_interact_obj(interact_obj):
    interact_obj_list.append(interact_obj)


def interact_to_obj(player_idx):
    small_len_obj = None
    small_len = 30000
    for a in interact_obj_list:
        if player_idx == 1:
            _pos = mouse_pos_to_world(player1_controller.pos, views[0])
            _pos[1] -= 150
        elif player_idx == 2:
            _pos = player2.pos
        _vec = _pos - a.pos
        _len = sum(x*x for x in _vec)
        if _len < small_len:
            small_len = _len
            small_len_obj = a
            small_len_obj.interact_input(player_idx)
            return


class Player2(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, views, np.array([80, 0]))
        self.anim.load('img/user_walk.png', 1, 8, views, np.array([80, 0]))
        self.anim.load('img/user_run.png', 1, 4, views, np.array([80, 0]))
        self.anim.load('img/user_active.png', 3, 3, views, np.array([80, 0]))  # 3
        self.pos[1] = floor_height[1]
        self.interact_obj = None #있을 때 움직이면 인터렉트 오브젝트 비활성화 용
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
        if self.interact_obj != None or self.is_in_stair:
            return
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)


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
        _len = sum(x*x for x in _pos)
        if _len < 15000:
            return True
        return False

    def send_player(self, input_idx, my_idx): #input_idx 0:w 1:a 2:s 3:d
        if input_idx == 0:
            if my_idx % 3 == 0 and my_idx < 12:
                return;
            if my_idx >= 12 and my_idx % 3 == 0:
                player2.pos = cp.copy(stair_list[my_idx - 10].pos)
            else:
                player2.pos = cp.copy(stair_list[my_idx - 1].pos)
        elif input_idx == 2:
            if my_idx % 3 == 2 and my_idx >= 12:
                return;
            if my_idx < 12 and my_idx % 3 == 2:
                player2.pos = cp.copy(stair_list[my_idx + 10].pos)
            else:
                player2.pos = cp.copy(stair_list[my_idx + 1].pos)

        elif input_idx == 1:
            if 6 <= my_idx <= 8 or 6+12 <= my_idx <= 8+12: #옆방으로
                player2.pos = cp.copy(stair_list[my_idx - 3].pos)
            else:
                player2.pos = cp.copy(self.pos)
                if 0 <= my_idx <= 2 or 0 + 12 <= my_idx <= 2 + 12:
                    pass
                else:
                    player2.pos[0] -= 150
                player2.is_in_stair = False
        elif input_idx == 3:
            if 3 <= my_idx <= 5 or 3+12 <= my_idx <= 5+12: #옆방으로
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
    def __init__(self, objm, doing_limit_time=-1):
        super().__init__(objm)
        self.anim = Animator()
        self.pos[1] = -139
        self.doing_remain_time = 0
        self.doing_limit_time = doing_limit_time #0 이상이면 키는 시간이 존재함
        self.is_playing_doing = False
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

    def interact(self, player_idx, is_interacting=False):
        if player_idx == 1:
            self.anim.play(0)
            print(1)
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

    def interact_input(self, player_idx):
        assert player_idx != 0, "player_idx != 0"
        if player_idx == 1:
            _pos = mouse_pos_to_world(player1_controller.pos, views[0])
            _pos[1] -= 150
        elif player_idx == 2:
            _pos = player2.pos
        #_size = self.anim.get_size()
        #_hsize = (_size[0] + _size[1])//2
        _hsize = 110
        _min_length = 10000
        _tem_pos = np.array([self.pos[0], self.pos[1]])
        for h in floor_height:
            _len = abs(abs(_pos[1] - self.pos[1]) - abs(h - self.pos[1]))
            if _len < _min_length:
                _min_length = _len
                _tem_pos[1] = h
        _x = (_tem_pos - _pos)
        _len_2 = sum(i ** 2 for i in _x)
        _hsize2 = _hsize * _hsize
        _hsize2 += _hsize2
        print(_pos, _tem_pos, _len_2, _hsize2)
        if _len_2 < _hsize2:
            self.interact(player_idx)

def calculate_floor_height(floor):
    return floor_height[floor%3] + 1080 if floor >= 3 else floor_height[floor]

# 층은 0층부터 시작
def make_obj(name, x, floor):
    t = InteractObj(firstScene.objM)
    t.pos[0] = x
    t.pos[1] = calculate_floor_height(floor)
    if name == '에어컨':
        t.pos[1] += 100
    t.anim.load('img/'+name+'_off.png', 1, 1, views, np.array([0, 0]))
    if name == '복사기':
        t.anim.load('img/복사기_on.png', 1, 4, views, np.array([0, 0]))
        t.anim.load('img/복사기_start.png', 1, 2, views, np.array([0, 0]))
    else:
        t.anim.load('img/'+name+'_on.png', 1, 2, views, np.array([0, 0]))

obj_name_list = ['냉장고', '복사기', '에어컨', '전등', '정수기', '컴터']

def make_random_floor_obj(x, floor):
    i = 0
    wall_size = 600
    count = random.randint(2,4)
    range = (1920-wall_size*2)//count
    small_range = range // 10
    while i < count:
        make_obj(obj_name_list[random.randint(0, len(obj_name_list) - 1)], x*1920-1920//2+wall_size+range*i + random.randint(-small_range, small_range), floor)
        i += 1

def init():
    pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE) # 마우스 화면밖에 못나가게
    pc.SDL_WarpMouseInWindow(views[0].window, views[0].w//2, views[0].h//2)

    global buildings
    buildings = []
    building_pos = [[0, 1080], [1920, 1080],[0, 0],[1920, 0]]
    i = 0
    while i < 4:
        buildings.append(Building(firstScene.objM))
        buildings[i].pos = np.array(building_pos[i])
        for y in floor_height:
            stair = Stair(firstScene.objM)
            stair.set_pos(-649+buildings[i].pos[0], y+buildings[i].pos[1])
        for y in floor_height:
            stair = Stair(firstScene.objM)
            stair.set_pos(540+buildings[i].pos[0], y+buildings[i].pos[1])
            stair.imgs[1].filp = stair.imgs[0].filp = True
        i+=1

    i=0
    while i < 3:
        stair_list[i + 3].other_stair = stair_list[i + 6]
        stair_list[i + 6].other_stair = stair_list[i + 3]
        stair_list[i + 3+12].other_stair = stair_list[i + 6+12]
        stair_list[i + 6+12].other_stair = stair_list[i + 3+12]
        i+=1

    # Make Obj
    i = 0
    while i < 6:
        make_random_floor_obj(0, i)
        i += 1

    global player2
    player2 = Player2(firstScene.objM)

    cursor = Cursor(firstScene.objM)
    cursor.load_img('img/cursor.png', views)


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
            print(a.key)
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
