from PicoModule import *
import GamePlay
import GameManager
from Building import Building
import random
import copy as cp
from InteractObj import InteractObj
from Actor import Actor
from Sound import Sound


class Player(DrawObj):
    KEY_W, KEY_A, KEY_S, KEY_D = -2, -1, 2, 1
    IDLE, WALK, RUN, ACTIVE, DIE, MOVEBODY, ATTACK, HIT = range(8)
    g_id = 0

    @classmethod
    def RESET(cls):
        cls.g_id = 0

    def __init__(self):
        super().__init__()
        self.load_img('img/stair_move.png')
        self.anim2 = Animator()
        self.anim2.load('img/ping.png', 1, 2, np.array([0, 0]))
        self.size[0], self.size[1] = 1, 1
        self.anim = Animator()
        self.anim.load('img/user_idle.png', Animator.TYPE_REPEAT, 5, np.array([80, 0]))  # 0
        self.anim.load('img/user_walk.png', Animator.TYPE_REPEAT, 8, np.array([80, 0]))  # 1
        self.anim.load('img/user_run.png', Animator.TYPE_REPEAT, 4, np.array([80, 0]))  # 2
        self.anim.load('img/user_active.png', Animator.TYPE_ONCENEXTPLAY, 3, np.array([80, 0]))  # 3
        self.anim.load('img/user_die1.png', Animator.TYPE_ONCE, 9, np.array([80, 0]))  # 4 플레이어한테 죽음
        self.anim.load('img/user_movebody.png', Animator.TYPE_ONCE, 7, np.array([0, 0]))  # 5 시체유기
        self.anim.load('img/user_attack.png', Animator.TYPE_ONCENEXTPLAY, 7, np.array([0, 0]))  # 6 공격
        self.anim.load('img/user_hit.png', Animator.TYPE_ONCENEXTPLAY, 1, np.array([80, 0]))  # 7 아야
        self.anim.anim_arr[7].delayTime = 1 / 2.0

        self.attack_sound = Sound.load('sound/Attack2.wav', 100)
        self.interact_sound = Sound.load('sound/빰.wav', 100)
        self.hurt_sound = Sound.load('sound/영훈_아야.wav', 100)
        self.movebody_sound = Sound.load('sound/GetBody.wav', 100)
        self.die_sound = Sound.load('sound/Die.wav', 100)

    def init(self, name):
        random_x = (0, 1920)
        self.name = name
        self.pos[0] = random_x[random.randint(0, 1)]
        self.pos[1] = GamePlay.calculate_floor_height(random.randint(0, 5))
        self.interact_obj = None  # 있을 때 움직이면 인터렉트 오브젝트 비활성화 용
        self.is_in_stair = False
        self.health = 2
        self.is_paused = False
        self.prev_pos = cp.copy(self.pos)
        self.delta_pos = np.array([0, 0])
        self.debug_attack_pos = [0, 0]
        self.id = Player.g_id
        Player.g_id += 1
        self.dead_remove_remain_time = 2

        self.is_attacking = False
        self.moving_body = None

        viewIdx = len(View.views) - 1
        self.half_w = View.views[viewIdx].w // 2
        self.half_h = View.views[viewIdx].h // 2
        # View.views[viewIdx].cam.pos = self.pos - np.array([self.half_w, self.half_h - 200])

    def attack(self):
        print(self.id, ": attack")
        self.anim.play(Player.ATTACK, Player.IDLE)
        self.attack_sound.play()

    def hit(self):
        print(self.id, ": hit")
        self.anim.play(Player.HIT, Player.IDLE)
        self.hurt_sound.play()
        self.health -= 1
        if self.is_die():
            self.die()

    def interact(self):
        print(self.id, ": interact")
        self.anim.play(Player.ACTIVE, Player.IDLE)
        self.interact_sound.play()
        self.cancel_move_body()

    def update_pos(self, pos):
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.delta_pos = self.pos - self.prev_pos
        self.prev_pos = cp.copy(self.pos)

    def tick(self, dt):
        if self.id == GameManager.g_my_player_id:
            self.update_camera(dt)
        self.anim2.tick(dt)  # 머리위에 핑 애니메이션

        end_anim_idx = self.anim.tick(dt)

        if self.is_die() and end_anim_idx == ISONCEEND and not self.is_paused:  # 죽는게 끝나면
            print("키보드 플레이어 죽음")
            if GameManager.g_my_player_id == self.id:
                GameManager.boardcast_win_player(-1)
            self.is_paused = True
            # GameManager.round_end(1)
            return
        if self.is_die():
            self.dead_remove_remain_time -= dt
            if self.dead_remove_remain_time <= 0:
                GameManager.remove_player(self)
            return

        if self.anim.anim_idx == Player.HIT:
            return

        # if self.anim.anim_idx == Player.ATTACK:
        #     if not self.is_attacking:  # 맞는동작중엔 아무것도못하게
        #         if self.anim.anim_arr[self.anim.anim_idx].frame >= 5:
        #             # 일정이상 프레임넘어가면 공격함
        #             self.attack()
        #             self.is_attacking = True
        #     return

        self.is_attacking = False

        speed = 300
        # print("x delta: ", self.delta_pos[0], ", move speed: ", np.linalg.norm(self.delta_pos))

        # 상호작용
        run = KeyController.moveTime.check(dt)  # s키 동작 상태확인
        if run == TimePassDetector.CLICK:
            # 인터렉트
            pass
        else:
            if self.moving_body is not None:
                speed = 100
            delta_move_length = np.linalg.norm(self.delta_pos)
            if delta_move_length <= 50*dt:
                if self.anim.is_end:
                    if self.moving_body is None:
                        self.anim.play(0)
            else: # 이동중임
                if self.interact_obj is not None:
                    self.interact_obj.cancel_by_move()
                if delta_move_length > speed*dt*1.4:
                    self.anim.play(Player.RUN)
                    self.cancel_move_body()
                else:
                    if self.moving_body is None:
                        self.anim.play(Player.WALK)
                if self.moving_body is None:
                    if self.delta_pos[0] > 0:
                        self.anim.flip = 'h'
                    elif self.delta_pos[0] < 0:
                        self.anim.flip = ''
                else:
                    if self.delta_pos[0] > 0:
                        self.anim.flip = ''
                    elif self.delta_pos[0] < 0:
                        self.anim.flip = 'h'

        # if end_anim_idx == Player.ACTIVE:
        #     InteractObj.interact_to_obj(2)
        # elif end_anim_idx == Player.DIE:  # 죽고나면 게임 끝
        #     GameManager.round_end(1)

        self.check_stair()  # 계단에 부딪혔는지 확인

    def check_take_damage(self, point):
        if self.is_die():
            return

        size = np.array([45, 200])
        x1, y1 = self.pos[0] - size[0], self.pos[1] + size[1]
        x2, y2 = self.pos[0] + size[0], self.pos[1]
        rect = (x1, y1, x2, y2)

        if collide_rect_point(rect, point):
            self.anim.play(7, 0)
            self.health -= 1
            self.hurt_sound.play()
            if self.is_die():
                self.die()
            return True
        return False

    def cancel_move_body(self):
        if self.moving_body is not None:
            self.moving_body.move_body(None)
        self.moving_body = None

    def die(self):
        print(self.id, ": die")
        self.health = 0
        self.die_sound.play()
        self.anim.play(4)

    # tick 에서 불림 계단이랑 부딫히면 계단안에 들어간 상태로 변경
    def check_stair(self):
        # if self.is_in_stair:
        #     return

        i = 0
        t_count = len(Building.stairs)
        while i < t_count:
            if Building.stairs[i].check_player_pos(self.pos):
                self.is_in_stair = True
                # if self.moving_body is not None:
                #     self.moving_body.is_in_stair = True
                #     self.cancel_move_body()
                return
            i += 1
        self.is_in_stair = False

    # 계단 안에서 움직이기
    def move_stair(self, input_key):
        if not self.is_in_stair:
            if input_key == Player.KEY_W:
                if self.moving_body is not None:
                    self.cancel_move_body()
                    return
                actor, distance = Actor.get_shortest_actor(self.pos)
                if actor.is_die_anim_end:
                    if distance < 150 * 150:
                        actor.move_body(self)
                        self.movebody_sound.play()
                        self.moving_body = actor
                        self.anim.play(Player.MOVEBODY)
                else:
                    if self.anim.anim_idx is not Player.ATTACK:
                        self.attack_sound.play()
                        self.anim.play(Player.ATTACK, Player.IDLE)
            return
        i = 0
        t_count = len(Building.stairs)
        while i < t_count:
            if Building.stairs[i].check_player_pos(self.pos):
                Building.stairs[i].send_player(input_key, i)
                return
            i += 1

    def update_camera(self, dt):
        player_pos = np.array([self.pos[0] - self.half_w, self.pos[1] - self.half_h + 100])
        cam = View.views[0].cam
        cam_pos = cam.pos

        # 카메라가 최종 승리자에게 초점이 맞춰짐
        if GameManager.is_game_end():
            zero = Camera.center
            cam_pos += (zero - cam_pos) * dt * 3
            cam.size += (cam.default_size * 0.45 - cam.size) * dt * 2

            cam = View.views[0].cam
            cam_pos = cam.pos
            cam_pos += (zero - cam_pos) * dt * 3
            cam.size += (cam.default_size * 0.45 - cam.size) * dt * 2
        else:
            half_w, half_h = np.array(get_center()) // 2
            cam_offset = 1920 // 4 - half_w, 1080 // 4 - half_h
            cam_pos += (player_pos - cam_offset - cam_pos) * dt * 3

    def render(self, cam):
        # if self.interact_obj is not None:
        #     return
        tem_pos, tem_size = self.calculate_pos_size(cam)

        if self.is_in_stair:  # 계단안에 있다면 플레이어2에게만 화살표로 표시하고 나머지에겐 안보임
            tem_pos[1] += 150* cam.size
            self.imgs[0].render(tem_pos, tem_size)
            return

        self.anim.render(tem_pos, tem_size, cam)

        tem_pos[1] += 190 * cam.size
        self.anim2.render(tem_pos, tem_size, cam)  # 머리위에 표시되는 핑

        import Font
        Font.active_font(0, True)
        tem_pos[1] += 50 * cam.size
        Font.draw_text(str(self.name), tem_pos)

        tem_pos = (self.debug_attack_pos - cam.pos) * cam.size

    def is_die(self):
        return self.health <= 0
