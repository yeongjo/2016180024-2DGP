from PicoModule import *
from GamePlay import *

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

    def clear_actors():
        actor_list = Actor.actor_list
        for a in actor_list:
            ObjsList.active_list.remove_object(a)
        actor_list.clear()

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