from PicoModule import *
from GamePlay import *

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