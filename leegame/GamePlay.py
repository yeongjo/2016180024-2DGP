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



# 활성화 된 오브젝트 리스트를 가지고
# UI 상태 값에 업데이트 시켜준다.
class GameManger:
    __remain_time = 1
    __wait_time = 1

    __scene_state = 1  # 게임화면

    @classmethod
    def init(cls, player_uis):
        cls.player_uis = player_uis
        cls.player1_damage_amount = 0.01  # 100초 초당한번씩하면
        cls.player2_damage_amount = 0  # 활성화된 오브젝트갯수에 따라 달라짐

    @classmethod
    def update(cls, dt):
        if cls.__scene_state is not 1: return
        cls.__remain_time -= dt
        if cls.__remain_time <= 0:
            cls.__remain_time += cls.__wait_time
            cls.update_damage()

    @classmethod
    def increase_player2_damage(cls, damage):
        cls.player2_damage_amount += damage

    @classmethod
    def update_damage(cls):
        cls.player_uis[0].take_damage(cls.player1_damage_amount)
        cls.player_uis[1].take_damage(cls.player2_damage_amount)

    # UI에 수치가 있고 거기서 종료여부를 판단해서 받는다
    @classmethod
    def game_end(cls, idx):
        # TODO 게임 끝나는 상태로 변경
        if idx == 1:
            print("마우스 승리")
            pass  # 마우스
        else:
            print("키보드 승리")
            pass  # 키보드


from Player2 import Player2
from Stair import Stair
from InteractObj import InteractObj


class Cursor(DrawObj):

    def __init__(self):
        super().__init__()
        self.anim = Animator()
        self.target_cam_pos = np.array([0, 0])
        self.mouse = [0, 0]

    def tick(self, dt):
        global MouseController
        pos = MouseController.pos
        speed = 1500
        img_size = self.anim.anim_arr[0].get_size()
        
        self.mouse = mouse_pos_to_world(pos, View.views[0])
        self.pos = self.mouse + np.array([img_size[0] / 2, -img_size[1] / 2])

        if MouseController.is_down is False:
            if self.anim.anim_idx == 2:
                self.shot()
            elif self.anim.anim_idx != 3:
                self.anim.play(0)

        anim_end_idx = self.anim.tick(dt)

        # 카메라 텔레포트방지
        if dt * speed > 500:
            return

        if pos[0] < 20:
            View.views[0].cam.pos[0] -= dt * speed
            t_size = -MAP_HALF_WIDTH
            if View.views[0].cam.pos[0] < t_size:
                View.views[0].cam.pos[0] = t_size
        elif pos[0] > View.views[0].w - 20:
            View.views[0].cam.pos[0] += dt * speed
            t_size = MAP_HALF_WIDTH
            if View.views[0].cam.pos[0] > t_size:
                View.views[0].cam.pos[0] = t_size
        if pos[1] < 20:
            View.views[0].cam.pos[1] += dt * speed
            t_size = MAP_HALF_HEIGHT
            if View.views[0].cam.pos[1] > t_size:
                View.views[0].cam.pos[1] = t_size
        elif pos[1] > View.views[0].h - 20:
            View.views[0].cam.pos[1] -= dt * speed
            t_size = -MAP_HALF_HEIGHT
            if View.views[0].cam.pos[1] < t_size:
                View.views[0].cam.pos[1] = t_size

        # 마우스 끝에 가져다 대기만하면 다른 칸으로 이동
        # if pos[0] < 20:
        #     self.target_cam_pos[0] = -MAP_WIDTH//2
        # if pos[0] > active_view_list[0].w - 20:
        #     self.target_cam_pos[0] = MAP_WIDTH//2
        # if pos[1] < 20:
        #     self.target_cam_pos[1] = MAP_HEIGHT//2
        # if pos[1] > active_view_list[0].h - 20:
        #     self.target_cam_pos[1] = -MAP_HEIGHT//2
        #
        # delta = self.target_cam_pos - active_view_list[0].cam.pos
        # active_view_list[0].cam.pos += (delta) * (dt * speed)

        check_state = MouseController.clickTime.check(dt)
        if check_state == 1:
            InteractObj.interact_to_obj(1)
        elif check_state == 2 and self.anim.anim_idx == 0:
            self.anim.play(1, 2)

    def shot(self):
        self.anim.play(3, 0)

        if Player2.this.check_take_damage(self.mouse) is False:
            small_len_obj = None
            small_len = 300000000
            tem_mouse_pos = np.array([self.mouse[0], self.mouse[1] - 150])

            actor_list = Actor.actor_list
            for a in actor_list:
                _vec = tem_mouse_pos - a.pos
                _len = sum(x * x for x in _vec)
                if _len < small_len:
                    small_len = _len
                    small_len_obj = a

            if small_len_obj is not None:
                small_len_obj.check_take_damage(self.mouse)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        img_size = self.anim.anim_arr[0].get_size()
        debug_text(str(self.pos + np.array([-img_size[0] // 2, img_size[1] // 2])), tem_pos)







class ActorBrain:
    def __init__(self, actor, x):
        self.__remain_time = random.uniform(1.5, 3.3)
        self.next_waypoint = actor.pos[0]
        self.waypoint_limit = (actor.pos[0], actor.pos[0])
        self.actor = actor
        self.is_move_finished = True
        self.stair_wait_remain_time = 1
        self.is_in_stair = False

        self.set_waypoint_limit(x)

    # x: (-range, range) 튜플
    def set_waypoint_limit(self, x):
        self.waypoint_limit = x
        self.next_waypoint = random.uniform(self.waypoint_limit[0], self.waypoint_limit[1])
        self.is_move_finished = False
        self.is_next_waypoint_stair = False

    def tick(self, dt):
        self.__move_stair(dt)
        if self.is_move_finished is False and self.is_in_stair is False:
            self.__move_to(dt)
            return

        self.__remain_time -= dt
        if self.__remain_time <= 0:
            self.__remain_time = random.uniform(1.5, 5.3)
            if random.random() > 0.3:
                self.next_waypoint = random.uniform(self.waypoint_limit[0], self.waypoint_limit[1])
            else:
                self.next_waypoint = self.waypoint_limit[0] if random.random() > 0.5 else self.waypoint_limit[1]
                self.is_next_waypoint_stair = True
            self.is_move_finished = False

    def __go_in_stair(self):
        self.actor.change_go_in_stair(True)
        self.is_in_stair = True
        self.stair_wait_remain_time = random.uniform(1, 3)

    def __move_stair(self, dt):
        if self.is_in_stair is False:
            return
        self.stair_wait_remain_time -= dt

        # 계단에 있다 시간이 다되면 계단에서 나온다.
        if self.stair_wait_remain_time < 0:
            self.is_next_waypoint_stair = self.is_in_stair = False
            self.actor.change_go_in_stair(False)
            self.actor.pos[1] = calculate_floor_height(random.randint(0, 6))
            self.__remain_time = 0  # 계단에서 나오고 바로 움직인다.

    def __move_to(self, dt):
        delta_x = self.next_waypoint - self.actor.pos[0]
        x = 1 if delta_x > 0 else -1
        if abs(delta_x) < self.actor.speed * dt * 2:
            self.is_move_finished = True
            if self.is_next_waypoint_stair:
                self.__go_in_stair()
                return

            self.actor.move(0, False)
            return

        self.actor.move(dt * x, False)


class Actor(DrawObj):
    actor_list = []

    def __init__(self):
        super().__init__()
        self.size[0], self.size[1] = 1, 1
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, np.array([80, 0]))
        self.anim.load('img/user_walk.png', 1, 8, np.array([80, 0]))
        self.anim.load('img/user_run.png', 1, 4, np.array([80, 0]))
        self.anim.load('img/user_die1.png', 2, 9, np.array([80, 0]))  # 3 플레이어한테 죽음
        self.anim.load('img/user_hit.png', 3, 1, np.array([80, 0]))  # 4 아야
        self.speed = 300
        self.is_die = False
        self.is_in_stair = False
        self.health = 1

        Actor.actor_list.append(self)

    def set_brain(self, brain):
        self.brain = brain

    def tick(self, dt):
        end_anim_idx = self.anim.tick(dt)
        if self.is_die:
            return
        self.brain.tick(dt)

    # 뇌가 조종함
    def move(self, x, is_run):
        if self.is_die:
            return
        if x > 0:
            self.anim.flip = 'h'
            self.anim.play(1)
        elif x < 0:
            self.anim.flip = ''
            self.anim.play(1)
        else:
            self.anim.play(0)

        self.pos[0] += x * self.speed

    def change_go_in_stair(self, val):
        self.is_in_stair = val

    def render(self, cam):
        if self.is_in_stair:
            return

        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.health), tem_pos)

    def check_take_damage(self, point):
        if self.is_die or self.is_in_stair:
            return

        size = np.array([90 // 2, 199 // 2])   # 충돌범위 따로 지정
        rect = (self.pos[0] - size[0], self.pos[1] + size[1], self.pos[0] + size[0], self.pos[1] - size[1])
        if collide_rect_point(rect, point):
            self.health -= 1
            if self.health <= 0:
                self.health = 0
                self.die()
            return True
        return False

    def die(self):
        self.is_die = True
        self.anim.play(4, 3)
        Actor.actor_list.remove(self)


class Building(DrawObj):
    def __init__(self):
        super().__init__()
        self.load_img('img/map.png')


# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor % 3] + MAP_HEIGHT if floor >= 3 else EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING[floor]


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


obj_name_list = ['냉장고', '복사기', '에어컨', '전등', '정수기', '컴터']


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


class Ui(DrawObj):

    def __init__(self):
        super().__init__()
        self.off = (0, 0)

    def set_off(self, off):
        self.off = off

    def render(self, cam):
        

        vw = View.views[cam.idx].w // 2
        vh = View.views[cam.idx].h
        ratio1 = View.views[cam.idx].w / MAP_WIDTH
        ww = self.imgs[0].size[0] // 2 * 1.5 * ratio1
        # h = active_view_list[cam.idx].h / MAP_HEIGHT
        tem_size = np.array([ratio1, ratio1])
        tem_pos = np.array([self.pos[0] * ratio1 + vw - self.off[0] * ww, vh - self.pos[1] * ratio1])
        tem_size *= 1.5
        self.imgs[cam.idx].render(tem_pos, tem_size)


class UiHp(DrawObj):

    def init(self, r, g, b, idx, side_img_pos):
        self.color = (r, g, b)
        self.idx = idx
        self.__hp_max_x = 369 * idx
        self.value = 1
        self.side_img_pos = side_img_pos

    def render(self, cam):
        vw = View.views[cam.idx].w // 2
        vh = View.views[cam.idx].h
        ratio1 = View.views[cam.idx].w / MAP_WIDTH
        # h = active_view_list[cam.idx].h / MAP_HEIGHT
        tem_size = np.array([self.size[0] * ratio1 + vw, vh - self.size[1] * ratio1])
        tem_pos = np.array([self.value * self.__hp_max_x * ratio1 + vw, vh - self.pos[1] * ratio1])
        fill_rectangle(tem_pos[0], tem_pos[1], tem_size[0], tem_size[1], self.color[0], self.color[1],
                              self.color[2])

    def take_damage(self, amount):
        self.value -= amount
        self.side_img_pos[0] = self.value * self.__hp_max_x + self.idx * -3
        if self.value <= 0:
            self.value = 0
            # call end
            GameManger.game_end(self.idx)


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
    ui_hp1 = UiHp()
    ui_hp1.set_pos(-369, 64)
    ui_hp1.size[0], ui_hp1.size[1] = 0, 35
    ui_hp1.init(240, 63, 63, -1.0, ui_keyboard.pos)

    ui_hp2 = UiHp()
    ui_hp2.set_pos(369, 64)
    ui_hp2.size[0], ui_hp2.size[1] = 0, 35
    ui_hp2.init(91, 215, 232, 1.0, ui_mouse.pos)

    ui_center = Ui()
    ui_center.load_img('img/ui_center.png')
    ui_center.set_pos(0, 90)

# -----------------------------------main code start-----------------------------------

def enter():
    #pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE)  # 마우스 화면밖에 못나가게
    
    pc.SDL_WarpMouseInWindow(View.views[0].window, View.views[0].w // 2, View.views[0].h // 2)
    
    global objsList
    if objsList == None:
        objsList = ObjsList()
    objsList.active()

    make_objs()

    GameManger.init((ui_hp2, ui_hp1))


def update(dt):  # View 각자의 그리기를 불러줌
    GameManger.update(dt)
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

        # 마우스 입력
        if a.type == pc.SDL_MOUSEBUTTONDOWN and a.button == 1:
            MouseController.interact_input(True)
        if a.type == pc.SDL_MOUSEMOTION:
            MouseController.mouse_input(a.x, a.y)

        if a.type == pc.SDL_MOUSEBUTTONUP and a.button == 1:
            MouseController.interact_input(False)

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

            # ESC 게임 종료
            elif a.key == pc.SDLK_ESCAPE:
                game_framework.quit()

        if a.type == pc.SDL_KEYUP:
            if a.key == 97:  # a
                KeyController.x += 1
            if a.key == 100:  # d
                KeyController.x -= 1
            if a.key == 115:  # s
                KeyController.interact_input(False)
