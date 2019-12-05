from PicoModule import *
from GamePlay import *
from Sound import Sound

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
        self.is_die_anim_end = False
        self.is_in_stair = False
        self.health = 1

        self.hurt_sound = Sound.load('sound/영훈_욱.wav', 100)

        self.player = None

        Actor.actor_list.append(self)

    @classmethod
    def clear_actors(cls):
        actor_list = Actor.actor_list
        for a in actor_list:
            ObjsList.active_list.remove_object(a)
        actor_list.clear()

    @classmethod
    def get_shortest_actor(self, point):
        small_len_obj = None
        small_len = 300000000
        tem_mouse_pos = np.array([point[0], point[1]])

        actor_list = Actor.actor_list
        for a in actor_list:
            _vec = tem_mouse_pos - a.pos
            _len = sum(x * x for x in _vec)
            if _len < small_len:
                small_len = _len
                small_len_obj = a

        return small_len_obj, small_len

    @classmethod
    def take_damage_shortest_point(cls, point):
        a, dis = cls.get_shortest_actor(point)
        if a is not None:
            a.check_take_damage(point)

    def set_brain(self, brain):
        self.brain = brain

    def move_body(self, player):
        self.player = player

    def tick(self, dt):
        self.anim.tick(dt)
        if self.is_die:
            if self.anim.anim_idx == 3 and self.anim.is_end:
                self.is_die_anim_end = True
            if self.player is not None:
                self.pos = cp.copy(self.player.pos)
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
        if self.is_in_stair or self.player is not None:
            return

        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        debug_text(str(self.health), tem_pos)

    def check_take_damage(self, point):
        if self.is_die or self.is_in_stair:
            return
        size = np.array([45, 200])
        x1, y1 = self.pos[0] - size[0], self.pos[1] + size[1]
        x2, y2 = self.pos[0] + size[0], self.pos[1]
        rect = (x1, y1, x2, y2)

        if collide_rect_point(rect, point):
            self.take_damage()
            self.hurt_sound.play()
            return True
        return False

    def take_damage(self, team_kill=True):
        if self.is_die or self.is_in_stair:
            return
        self.health -= 1
        if self.health <= 0:
            self.health = 0
            self.die()
            if team_kill:
                GameManager.keyuser_ui.take_damage(0.2)

    def die(self):
        self.is_die = True
        self.anim.play(4, 3)