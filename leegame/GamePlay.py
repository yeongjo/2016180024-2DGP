from PicoModule import *
import game_framework
import Main
import copy as cp
import random

floor_height = (218, -139, -500)
map_size = (1920, 1080)

init_text()

player2 = None


def change_scene(scene):
    game_framework.change_state(scene)
    active_view_list[0].change_scene(scene)
    active_view_list[1].change_scene(scene)


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
        cls.player2_damage_amount = 0  # 가변가능

    @classmethod
    def update(cls, dt):
        if cls.__scene_state is not 1: return
        cls.__remain_time -= dt
        if cls.__remain_time <= 0:
            cls.__remain_time += cls.__wait_time
            cls.update_ui()

    @classmethod
    def increase_player1_damage(cls, damage):
        cls.player2_damage_amount += damage

    @classmethod
    def update_ui(cls):
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


actor_list = []


class Cursor(DrawObj):

    def __init__(self, objM):
        super().__init__(objM)
        self.anim = Animator()
        self.target_cam_pos = np.array([0, 0])
        self.mouse = [0, 0]

    def tick(self, dt):
        global Player1Controller
        pos = Player1Controller.pos
        speed = 1500
        img_size = self.anim.animArr[0].get_size()
        self.mouse = mouse_pos_to_world(pos, active_view_list[0])
        self.pos = self.mouse + np.array([img_size[0] / 2, -img_size[1] / 2])

        if Player1Controller.is_down is False:
            if self.anim.animIdx == 2:
                self.shot()
            elif self.anim.animIdx != 3:
                self.anim.play(0)

        anim_end_idx = self.anim.tick(dt)

        # active_view_list[1].cam.pos[0] = 500
        # 리스트 초기화를 클래스 안에서 함수없이 하니까 정적변수처럼되버림
        if dt * speed > 500:
            return
        if pos[0] < 20:
            active_view_list[0].cam.pos[0] -= dt * speed
            t_size = -map_size[0] // 2
            if active_view_list[0].cam.pos[0] < t_size: active_view_list[0].cam.pos[0] = t_size
        elif pos[0] > active_view_list[0].w - 20:
            active_view_list[0].cam.pos[0] += dt * speed
            t_size = map_size[0] // 2
            if active_view_list[0].cam.pos[0] > t_size: active_view_list[0].cam.pos[0] = t_size
        if pos[1] < 20:
            active_view_list[0].cam.pos[1] += dt * speed
            t_size = map_size[1] // 2
            if active_view_list[0].cam.pos[1] > t_size: active_view_list[0].cam.pos[1] = t_size
        elif pos[1] > active_view_list[0].h - 20:
            active_view_list[0].cam.pos[1] -= dt * speed
            t_size = -map_size[1] // 2
            if active_view_list[0].cam.pos[1] < t_size: active_view_list[0].cam.pos[1] = t_size

        # if pos[0] < 20:
        #     self.target_cam_pos[0] = -map_size[0]//2
        # if pos[0] > active_view_list[0].w - 20:
        #     self.target_cam_pos[0] = map_size[0]//2
        # if pos[1] < 20:
        #     self.target_cam_pos[1] = map_size[1]//2
        # if pos[1] > active_view_list[0].h - 20:
        #     self.target_cam_pos[1] = -map_size[1]//2
        #
        # delta = self.target_cam_pos - active_view_list[0].cam.pos
        # active_view_list[0].cam.pos += (delta) * (dt * speed)

        check_state = Player1Controller.clickTime.check(dt)
        if check_state == 1:
            interact_to_obj(1)
        elif check_state == 2 and self.anim.animIdx == 0:
            self.anim.play(1, 2)

    def shot(self):
        self.anim.play(3, 0)

        if player2.check_take_damage(self.mouse) is False:
            small_len_obj = None
            small_len = 300000000
            tem_mouse_pos = np.array([self.mouse[0], self.mouse[1] - 150])

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
        img_size = self.anim.animArr[0].get_size()
        debug_text(str(self.pos + np.array([-img_size[0] // 2, img_size[1] // 2])), tem_pos)


interact_obj_list = []


def add_interact_obj(interact_obj):
    interact_obj_list.append(interact_obj)


def interact_to_obj(player_idx):
    small_len_obj = None
    small_len = 300000000
    for a in interact_obj_list:
        if player_idx == 1:
            _pos = mouse_pos_to_world(Player1Controller.pos, active_view_list[0])
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

    # x 는 튜플임
    def set_waypoint_limit(self, x):
        self.waypoint_limit = x
        self.next_waypoint = random.uniform(self.waypoint_limit[0], self.waypoint_limit[1])
        self.is_move_finished = False
        self.is_next_waypoint_stair = False

    def tick(self, dt):
        self.__move_stair(dt)
        if self.is_move_finished is False and self.is_in_stair is False:
            self.move_to(dt)
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

    def go_in_stair(self):
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

    def move_to(self, dt):
        delta_x = self.next_waypoint - self.actor.pos[0]
        x = 1 if delta_x > 0 else -1
        if abs(delta_x) < self.actor.speed * dt * 2:
            self.is_move_finished = True
            if self.is_next_waypoint_stair:
                self.go_in_stair()
                return

            self.actor.move(0, False)
            return

        self.actor.move(dt * x, False)


class Actor(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.size[0], self.size[1] = 1, 1
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, views, np.array([80, 0]))
        self.anim.load('img/user_walk.png', 1, 8, views, np.array([80, 0]))
        self.anim.load('img/user_run.png', 1, 4, views, np.array([80, 0]))
        self.anim.load('img/user_die1.png', 2, 9, views, np.array([80, 0]))  # 3 플레이어한테 죽음
        self.anim.load('img/user_hit.png', 3, 1, views, np.array([80, 0]))  # 4 아야
        self.speed = 300
        self.is_die = False
        self.is_in_stair = False
        self.health = 1

        global actor_list
        actor_list.append(self)

    def set_brain(self, brain):
        self.brain = brain

    def tick(self, dt):
        end_anim_idx = self.anim.tick(dt)
        if self.is_die is True:
            return
        self.brain.tick(dt)

    # 뇌가 조종함
    def move(self, x, is_run):
        if self.is_die is True:
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
        if self.is_die is True:
            return

        size = np.array([90, 199]) // 2  # 충돌범위 따로 지정
        rect = (self.pos[0] - size[0], self.pos[1] + size[1], self.pos[0] + size[0], self.pos[1] - size[1])
        if check_coll_rect(rect, point):
            self.health -= 1
            if self.health <= 0:
                self.health = 0
                self.die()
            return True
        return False

    def die(self):
        self.is_die = True
        self.anim.play(4, 3)
        actor_list.remove(self)


class Player2(DrawObj):
    def __init__(self, objm):
        super().__init__(objm)
        self.load_img('img/stair_move.png', views)
        self.anim2 = Animator()
        self.anim2.load('img/ping.png', 1, 2, views, np.array([0, 0]))
        self.size[0], self.size[1] = 1, 1
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, views, np.array([80, 0]))  # 0
        self.anim.load('img/user_walk.png', 1, 8, views, np.array([80, 0]))  # 1
        self.anim.load('img/user_run.png', 1, 4, views, np.array([80, 0]))  # 2
        self.anim.load('img/user_active.png', 3, 3, views, np.array([80, 0]))  # 3
        self.anim.load('img/user_die1.png', 2, 9, views, np.array([80, 0]))  # 4 플레이어한테 죽음
        self.anim.load('img/user_movebody.png', 1, 7, views, np.array([80, 0]))  # 5 시체유기
        self.anim.load('img/user_attack.png', 3, 7, views, np.array([80, 0]))  # 6 공격
        self.anim.load('img/user_hit.png', 3, 1, views, np.array([80, 0]))  # 7 아야
        self.anim.animArr[7].delayTime = 1 / 2.0
        self.pos[1] = floor_height[1]
        self.interact_obj = None  # 있을 때 움직이면 인터렉트 오브젝트 비활성화 용
        self.is_in_stair = False
        self.health = 2
        self.is_die = False

        hw = active_view_list[1].w // 2
        hh = active_view_list[1].h // 2
        active_view_list[1].cam.pos = self.pos - np.array([hw, hh - 200])

    def tick(self, dt):
        global Player2Controller

        self.update_camera(dt)
        self.anim2.tick(dt)  # 머리위에 핑 애니메이션
        end_anim_idx = self.anim.tick(dt)

        if self.is_in_stair or self.is_die:  # 죽거나 계단안에 있으면 캐릭터 직접 조종불가
            return

        if self.anim.animIdx == 7:  # 맞는동작중엔 아무것도못하게
            return

        speed = 300

        run = Player2Controller.moveTime.check(dt)  # s키 동작 상태확인
        if run == 1:
            # 인터렉트
            self.anim.play(3, 0)
        else:
            if Player2Controller.x > 0:
                if self.interact_obj != None:
                    self.interact_obj.cancel_by_move()
                self.anim.flip = 'h'
                if run == 2:
                    self.anim.play(2)
                    speed *= 1.8
                else:
                    self.anim.play(1)
            elif Player2Controller.x < 0:
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

        self.pos[0] += Player2Controller.x * speed * dt
        if end_anim_idx == 3:
            interact_to_obj(2)
        elif end_anim_idx == 4:  # 죽고나면 게임 끝
            GameManger.game_end(1)

        self.check_stair()  # 계단에 부딪혔는지 확인

    def check_take_damage(self, point):
        if self.is_die is True:
            return

        size = np.array([90, 199]) // 2
        rect = (self.pos[0] - size[0], self.pos[1] + size[1], self.pos[0] + size[0], self.pos[1] - size[1])
        if check_coll_rect(rect, point):
            self.anim.play(7, 0)
            self.health -= 1
            if self.health <= 0:
                self.health = 0
                self.die()
            return True
        return False

    def die(self):
        self.is_die = True
        self.anim.play(4)

    # tick 에서 불림 계단이랑 부딫히면 계단안에 들어간 상태로 변경
    def check_stair(self):
        if self.is_die or self.is_in_stair:
            return

        i = 0
        t_count = len(stair_list)
        while i < t_count:
            if stair_list[i].check_player_pos(self.pos):
                self.is_in_stair = True
                # print("check_stair : true", stair_list[i].pos, self.pos)
                return
            i += 1

    # 계단 안에서 움직이기
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
        hw = active_view_list[1].w // 2
        hh = active_view_list[1].h // 2
        player_pos = np.array([self.pos[0] - hw, self.pos[1] - hh - 200])
        active_view_list[1].cam.pos += (player_pos - active_view_list[1].cam.pos) * dt * 3

    def render(self, cam):
        if self.interact_obj != None:
            return
        tem_pos, tem_size = self.calculate_pos_size(cam)

        if self.is_in_stair:  # 계단안에 있다면 플레이어2에게만 화살표로 표시하고 나머지에겐 안보임
            if cam.idx == 1:
                tem_pos[1] += 150
                self.imgs[1].render(tem_pos, tem_size)
            return

        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.health), tem_pos)

        if cam.idx == 0: return
        tem_pos[1] += 190
        self.anim2.render(tem_pos, tem_size, cam)  # 머리위에 표시되는 핑


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

    # 플레이어를 딴곳으로 보내줌
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
        # self.pos[1] = -139
        self.doing_remain_time = 0
        self.floor_y = None
        self.doing_limit_time = doing_limit_time  # 0 이상이면 키는 시간이 존재함
        self.is_playing_doing = False  # 플레이어가 키는시간이 있고 그 키는 시간중임을 표시
        self.damage = 0.01

        add_interact_obj(self)

    def tick(self, dt):
        self.anim.tick(dt)

        if self.is_playing_doing:
            self.doing_remain_time += dt
            if self.doing_limit_time < self.doing_remain_time and self.anim.animIdx is not 1:
                self.is_playing_doing = False
                self.anim.play(1)
                global player2
                player2.interact_obj = None
                GameManger.increase_player1_damage(self.damage)
                print("478 : player2 interact! : on tick")

    def cancel_by_move(self):
        if self.is_playing_doing == False:
            return
        self.is_playing_doing = False
        global player2
        player2.interact_obj = None
        self.anim.play(0)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.pos), tem_pos)
        debug_text(str(self.floor_y), tem_pos + np.array([0, 20]))

    def interact(self, player_idx, is_interacting=False):
        if player_idx == 1 and self.anim.animIdx is not 0:
            # Player1 Interact!!
            self.anim.play(0)
            GameManger.increase_player1_damage(-self.damage)
        elif player_idx == 2:
            if self.doing_limit_time >= 0 and self.anim.animIdx is not 1:
                # Player2 Interacting~~
                self.anim.play(2)
                self.doing_remain_time = 0
                self.is_playing_doing = True
                global player2
                player2.interact_obj = self
            elif self.anim.animIdx is not 1:
                print("508 : Player2 Interact!!")
                GameManger.increase_player1_damage(self.damage)
                self.anim.play(1)
            # else:
            #     self.anim.play(2)
            #     print('player2 interacting')

    # 이 오브젝트의 바닥위치 구하기
    def get_floor_pos(self):
        if self.floor_y is None:
            floor_offset = 0
            if self.pos[1] > map_size[1] // 2:
                t_pos_y = self.pos[1] - map_size[1]
                floor_offset = map_size[1]
            else:
                t_pos_y = self.pos[1]
            # self.floor_y = floor_height[0]
            for t in floor_height:
                self.floor_y = t + floor_offset
                if t <= t_pos_y:
                    break

        return np.array([self.pos[0], self.floor_y])

    def interact_input(self, player_idx, small_len):
        assert player_idx != 0, "player_idx != 0"
        if small_len < 150 * 150:
            self.interact(player_idx)


# 몇 층의 바닥의 높이가 얼마인지 받는 함수
def calculate_floor_height(floor):
    return floor_height[floor % 3] + map_size[1] if floor >= 3 else floor_height[floor]


# 층은 0층부터 시작
def make_obj(name, x, floor):
    t = InteractObj(objsList.objM)
    t.pos[0] = x
    t.pos[1] = calculate_floor_height(floor)
    if name == '에어컨':
        t.pos[1] += 100
    t.anim.load('img/' + name + '_off.png', 1, 1, views, np.array([0, 0]))
    if name == '복사기':
        t.anim.load('img/복사기_on.png', 1, 4, views, np.array([0, 0]))
        t.anim.load('img/복사기_start.png', 1, 2, views, np.array([0, 0]))
        t.doing_limit_time = 1.0
        t.damage *= 3
    else:
        t.anim.load('img/' + name + '_on.png', 1, 2, views, np.array([0, 0]))
    return t


obj_name_list = ['냉장고', '복사기', '에어컨', '전등', '정수기', '컴터']


def make_random_floor_obj(x, floor):
    wall_size = 400
    offset = x * map_size[0] - map_size[0] // 2
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

    def __init__(self, objM):
        super().__init__(objM)
        self.off = (0, 0)

    def set_off(self, off):
        self.off = off

    def render(self, cam):
        vw = active_view_list[cam.idx].w // 2
        vh = active_view_list[cam.idx].h
        ratio1 = active_view_list[cam.idx].w / map_size[0]
        ww = self.imgs[0].size[0] // 2 * 1.5 * ratio1
        # h = active_view_list[cam.idx].h / map_size[1]
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
        vw = active_view_list[cam.idx].w // 2
        vh = active_view_list[cam.idx].h
        ratio1 = active_view_list[cam.idx].w / map_size[0]
        # h = active_view_list[cam.idx].h / map_size[1]
        tem_size = np.array([self.size[0] * ratio1 + vw, vh - self.size[1] * ratio1])
        tem_pos = np.array([self.value * self.__hp_max_x * ratio1 + vw, vh - self.pos[1] * ratio1])
        pc.draw_fillrectangle(tem_pos[0], tem_pos[1], tem_size[0], tem_size[1], self.color[0], self.color[1],
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
        x = j * map_size[0]
        for i in range(6):
            for k in range(random.randint(0, 3)):
                brain_way_off = map_size[0] // 2 - 500
                actor = Actor(objsList)
                actor.pos[0] = random.uniform(x - brain_way_off, x + brain_way_off)
                actor.pos[1] = calculate_floor_height(i)
                brain = ActorBrain(actor, (x - brain_way_off, x + brain_way_off))
                actor.set_brain(brain)


# -----------------------------------main code start-----------------------------------

def enter():
    pc.SDL_SetRelativeMouseMode(pc.SDL_TRUE)  # 마우스 화면밖에 못나가게
    pc.SDL_WarpMouseInWindow(active_view_list[0].window, active_view_list[0].w // 2, active_view_list[0].h // 2)

    objsList = ObjsList()

    global buildings
    buildings = []
    building_pos = [[0, map_size[1]], [map_size[0] - 1, map_size[1]], [0, 0], [map_size[0] - 1, 0]]
    stair_pos_x = (649, 540)
    i = 0
    while i < 4:
        buildings.append(Building(objsList.objM))
        buildings[i].pos = np.array(building_pos[i])
        is_right = i % 2
        if is_right == 1:
            buildings[i].imgs[0].filp = True
            buildings[i].imgs[1].filp = True
        for y in floor_height:
            stair = Stair(objsList.objM)
            stair.set_pos(-stair_pos_x[0] + 18 * is_right + buildings[i].pos[0], y + buildings[i].pos[1])
        for y in floor_height:
            stair = Stair(objsList.objM)
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

    global player2
    player2 = Player2(objsList.objM)

    cursor = Cursor(objsList.objM)
    cursor.anim.load('img/cursor.png', 1, 1, views, np.array([0, 0]))
    cursor.anim.load('img/cursor_attack_start.png', 3, 4, views, np.array([0, 0]))
    cursor.anim.load('img/cursor_attack_doing.png', 1, 2, views, np.array([0, 0]))
    cursor.anim.load('img/cursor_attack_shot.png', 3, 1, views, np.array([0, 0]))

    ui_mouse = Ui(objsList.objM)
    ui_mouse.load_img('img/ui_mouse.png', views)
    ui_mouse.set_pos(366, 90)
    ui_mouse.set_off((-1, 0))

    ui_keyboard = Ui(objsList.objM)
    ui_keyboard.load_img('img/ui_keyboard.png', views)
    ui_keyboard.set_pos(-366, 90)
    ui_keyboard.set_off((1, 0))

    ui_hp1 = UiHp(objsList.objM)
    ui_hp1.set_pos(-369, 64)
    ui_hp1.size[0], ui_hp1.size[1] = 0, 35
    ui_hp1.init(240, 63, 63, -1.0, ui_keyboard.pos)

    ui_hp2 = UiHp(objsList.objM)
    ui_hp2.set_pos(369, 64)
    ui_hp2.size[0], ui_hp2.size[1] = 0, 35
    ui_hp2.init(91, 215, 232, 1.0, ui_mouse.pos)

    ui_center = Ui(objsList.objM)
    ui_center.load_img('img/ui_center.png', views)
    ui_center.set_pos(0, 90)

    GameManger.init((ui_hp2, ui_hp1))


def update(dt):  # View 각자의 그리기를 불러줌
    # active_view_list[0].cam.pos = mouse_pos_to_world(player1_controller.pos,active_view_list[0])
    GameManger.update(dt)
    active_view_list[0].tick(dt)
    active_view_list[0].render()
    active_view_list[1].render()


def handle_events():
    events = pc.get_events()
    for a in events:
        if a.type == pc.SDL_QUIT:
            game_framework.exit_game()

        # 마우스 입력
        if a.type == pc.SDL_MOUSEBUTTONDOWN and a.button == 1:
            Player1Controller.interact_input(True)
        if a.type == pc.SDL_MOUSEMOTION:
            Player1Controller.mouse_input(a.x, a.y)

        if a.type == pc.SDL_MOUSEBUTTONUP and a.button == 1:
            Player1Controller.interact_input(False)

        # 키보드 입력
        if a.type == pc.SDL_KEYDOWN:
            if a.key == 97:  # a
                Player2Controller.x -= 1
                player2.move_stair(1)
            if a.key == 100:  # d
                Player2Controller.x += 1
                player2.move_stair(3)
            if a.key == 115:  # s
                Player2Controller.interact_input(True)
                player2.move_stair(2)
            if a.key == 119:  # w
                player2.move_stair(0)

            # 카메라 줌 확인용
            if a.key == 61:
                active_view_list[0].cam.size += 0.5
            if a.key == 45:
                active_view_list[0].cam.size -= 0.5

            # ESC 게임 종료
            if a.key == 27:
                game_framework.exit_game()

        if a.type == pc.SDL_KEYUP:
            if a.key == 97:  # a
                Player2Controller.x += 1
            if a.key == 100:  # d
                Player2Controller.x -= 1
            if a.key == 115:  # s
                Player2Controller.interact_input(False)
