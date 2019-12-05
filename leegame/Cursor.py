from PicoModule import *
from GamePlay import *
from Actor import Actor
from Sound import Sound

class Cursor(DrawObj):

    def __init__(self):
        super().__init__(1)
        self.anim = Animator()
        self.target_cam_pos = np.array([0, 0])
        self.mouse_pos = [0, 0]

        self.anim.load('img/cursor.png', 1, 1, np.array([0, 0]))
        self.anim.load('img/cursor_attack_start.png', 3, 4, np.array([0, 0]))
        self.anim.load('img/cursor_attack_doing.png', 1, 2, np.array([0, 0]))
        self.anim.load('img/cursor_attack_shot.png', 3, 1, np.array([0, 0]))
        self.interact_sound = Sound.load('sound/Pop.wav', 100)
        self.shot_sound = Sound.load('sound/Duck Toy.wav', 100)

        detect_limit = 20
        self.leftLimit = detect_limit
        self.rightLimit = View.views[0].w - detect_limit
        self.topLimit = View.views[0].h - detect_limit
        self.bottomLimit = detect_limit

    def tick(self, dt):
        pos = MouseController.pos
        speed = 1500
        img_size = self.anim.anim_arr[0].get_size()
        
        self.mouse_pos = mouse_pos_to_world(pos, View.views[0])
        self.pos = self.mouse_pos + np.array([img_size[0] / 2 - 10, -img_size[1] / 2 - 30])

        if MouseController.is_down is False:
            if self.anim.anim_idx == 2:
                self.shot()
            elif self.anim.anim_idx != 3:
                self.anim.play(0)

        anim_end_idx = self.anim.tick(dt)

        # 카메라 텔레포트방지
        if dt * speed > 500:
            return
        
        # 라운드가 끝나면 카메라이동 자동으로 따라가게 둠
        if not GameManager.is_round_end:
            cam_pos = View.views[0].cam.pos

            # 마우스가 화면의 외곽선에 붙었는지 검사
            if pos[0] < self.leftLimit:
                cam_pos[0] -= dt * speed
                t_size = -MAP_HALF_WIDTH
                if cam_pos[0] < t_size:
                    cam_pos[0] = t_size
            elif pos[0] > self.rightLimit:
                cam_pos[0] += dt * speed
                t_size = MAP_HALF_WIDTH
                if cam_pos[0] > t_size:
                    cam_pos[0] = t_size
            if pos[1] < self.bottomLimit:
                cam_pos[1] += dt * speed
                t_size = MAP_HALF_HEIGHT
                if cam_pos[1] > t_size:
                    cam_pos[1] = t_size
            elif pos[1] > self.topLimit:
                cam_pos[1] -= dt * speed
                t_size = -MAP_HALF_HEIGHT
                if cam_pos[1] < t_size:
                    cam_pos[1] = t_size

        check_state = MouseController.clickTime.check(dt)
        if check_state == TimePassDetector.CLICK:
            InteractObj.interact_to_obj(1)
            self.interact_sound.play()
        elif check_state == TimePassDetector.ACTIVE and self.anim.anim_idx == 0:
            self.anim.play(1, 2)

    def shot(self):
        self.anim.play(3, 0)
        self.shot_sound.play()
        if Player2.this.check_take_damage(self.mouse_pos) is False:
            tem_pos = cp.copy(self.mouse_pos)
            # tem_pos[1] -= 150
            Actor.take_damage_shortest_point(tem_pos)

    def render(self, cam):
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.anim.render(tem_pos, tem_size, cam)
        img_size = self.anim.anim_arr[0].get_size()
        debug_text(str(self.pos + np.array([-img_size[0] // 2, img_size[1] // 2])), tem_pos)
