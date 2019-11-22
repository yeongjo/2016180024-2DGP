from PicoModule import *
from GamePlay import *

from InteractObj import InteractObj


class Player2(DrawObj):
    KEY_W, KEY_A, KEY_S, KEY_D = range(4)
    IDLE, WALK, RUN, ACTIVE, DIE, MOVEBODY, ATTACK, HIT = range(8)
    this = None

    def __init__(self):
        super().__init__()
        Player2.this = self
        self.load_img('img/stair_move.png')
        self.anim2 = Animator()
        self.anim2.load('img/ping.png', 1, 2, np.array([0, 0]))
        self.size[0], self.size[1] = 1, 1
        self.anim = Animator()
        self.anim.load('img/user_idle.png', 1, 5, np.array([80, 0]))  # 0
        self.anim.load('img/user_walk.png', 1, 8, np.array([80, 0]))  # 1
        self.anim.load('img/user_run.png', 1, 4, np.array([80, 0]))  # 2
        self.anim.load('img/user_active.png', 3, 3, np.array([80, 0]))  # 3
        self.anim.load('img/user_die1.png', 2, 9, np.array([80, 0]))  # 4 플레이어한테 죽음
        self.anim.load('img/user_movebody.png', 1, 7, np.array([80, 0]))  # 5 시체유기
        self.anim.load('img/user_attack.png', 3, 7, np.array([80, 0]))  # 6 공격
        self.anim.load('img/user_hit.png', 3, 1, np.array([80, 0]))  # 7 아야
        self.anim.anim_arr[7].delayTime = 1 / 2.0
        self.init()

    def init(self):
        random_x = (0, 1920)
        self.pos[0] = random_x[random.randint(0,1)]
        self.pos[1] = calculate_floor_height(random.randint(0, 5))
        self.interact_obj = None  # 있을 때 움직이면 인터렉트 오브젝트 비활성화 용
        self.is_in_stair = False
        self.health = 2
        self.is_die = False
        self.is_paused = False

        self.half_w = View.views[1].w // 2
        self.half_h = View.views[1].h // 2
        View.views[1].cam.pos = self.pos - np.array([self.half_w, self.half_h - 200])

    def tick(self, dt):

        self.update_camera(dt)
        self.anim2.tick(dt)  # 머리위에 핑 애니메이션
        end_anim_idx = self.anim.tick(dt)

        if self.is_die and end_anim_idx == ISONCEEND and not self.is_paused: # 죽는게 끝나면
            print("키보드 플레이어 죽음")
            self.is_paused = True
            GameManager.round_end(1)

        if self.is_in_stair or self.is_die or self.is_paused:  # 죽거나 계단안에 있으면 캐릭터 직접 조종불가
            return

        if self.anim.anim_idx == 7:  # 맞는동작중엔 아무것도못하게
            return

        speed = 300

        run = KeyController.moveTime.check(dt)  # s키 동작 상태확인
        if run == TimePassDetector.CLICK:
            # 인터렉트
            self.anim.play(3, 0)
        else:
            if KeyController.x == 0:
                if self.anim.is_end:
                    self.anim.play(0)
            else:
                if self.interact_obj is not None:
                    self.interact_obj.cancel_by_move()
                if run == TimePassDetector.ACTIVE:
                    self.anim.play(2)
                    speed *= 1.8
                else:
                    self.anim.play(1)
                if KeyController.x > 0:
                    self.anim.flip = 'h'
                elif KeyController.x < 0:
                    self.anim.flip = ''


        self.pos[0] += KeyController.x * speed * dt
        if end_anim_idx == 3:
            InteractObj.interact_to_obj(2)
        elif end_anim_idx == 4:  # 죽고나면 게임 끝
            GameManager.round_end(1)

        self.check_stair()  # 계단에 부딪혔는지 확인

    def check_take_damage(self, point):
        if self.is_die:
            return

        size = np.array([45, 200])
        x1, y1 = self.pos[0] - size[0], self.pos[1] + size[1]
        x2, y2 = self.pos[0] + size[0], self.pos[1]
        rect = (x1, y1, x2, y2)

        if collide_rect_point(rect, point):
            self.anim.play(7, 0)
            self.health -= 1
            if self.health <= 0:
                self.die()
            return True
        return False

    def die(self):
        self.is_die = True
        self.anim.play(4)

    # tick 에서 불림 계단이랑 부딫히면 계단안에 들어간 상태로 변경
    def check_stair(self):
        if self.is_in_stair:
            return

        i = 0
        t_count = len(stair_list)
        while i < t_count:
            if stair_list[i].check_player_pos(self.pos):
                self.is_in_stair = True
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
        player_pos = np.array([self.pos[0] - self.half_w, self.pos[1] - self.half_h + 100])
        cam = View.views[1].cam
        cam_pos = cam.pos


        # 카메라가 최종 승리자에게 초점이 맞춰짐
        if GameManager.is_round_end:
            zero = Camera.center
            cam_pos += (zero - cam_pos) * dt * 3
            cam.size += (cam.default_size*0.45 - cam.size) * dt * 2

            cam = View.views[0].cam
            cam_pos = cam.pos
            cam_pos += (zero - cam_pos) * dt * 3
            cam.size += (cam.default_size*0.45 - cam.size) * dt * 2
        else:
            cam_pos += (player_pos - cam_pos) * dt * 3

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

        if cam.idx == 0 and not GameManager.is_round_end: return
        tem_pos[1] += 190 * cam.size
        self.anim2.render(tem_pos, tem_size, cam)  # 머리위에 표시되는 핑