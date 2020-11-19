import pico2d as pc
import numpy as np
import os

is_debug = True

font01 = None

Screen_Width = 1920
Screen_Height = 1080


# 폰트 로딩
def load_defulat_font(text_path="font/HoonWhitecatR.ttf"):
    assert View.active_view != None  # pico2d 초기화하고나서 불러줘야함
    global font01
    font01 = pc.load_font(text_path, 55)


def fill_rectangle1(pos, size, r, g, b, a=255):
    x1 = pos[0] - size[0]//2
    y1 = pos[1] - size[1]//2
    x2 = pos[0] + size[0]//2
    y2 = pos[1] + size[1]//2
    fill_rectangle(x1, y1, x2, y2, r, g, b, a)


def fill_rectangle(x1, y1, x2, y2, r, g, b, a=255):
    view = View.active_view
    renderer = view.renderer
    pc.SDL_SetRenderDrawColor(renderer, r, g, b, a)
    rect = pc.SDL_Rect(int(x1), int(-y2 + view.h - 1), int(x2 - x1 + 1), int(y2 - y1 + 1))
    if (a != 255):
        pc.SDL_SetRenderDrawBlendMode(renderer, pc.SDL_BLENDMODE_BLEND)
    pc.SDL_RenderFillRect(renderer, rect)
    pc.SDL_SetRenderDrawBlendMode(renderer, pc.SDL_BLENDMODE_NONE)


# 디버그시에만 보임
def debug_text(str, pos, color=(0, 200, 0)):
    if (is_debug):
        draw_text(str, pos, color)


def draw_text(str, pos, color=(255, 255, 255)):
    global font01
    font01.draw(pos[0], pos[1], str, color)


def _open_other_canvas(w=int(800), h=int(600), sync=True, full=False):
    caption = ('2 (' + str(w) + 'x' + str(h) + ')').encode('UTF-8')
    if full:
        flags = pc.SDL_WINDOW_FULLSCREEN
    else:
        flags = pc.SDL_WINDOW_SHOWN

    window = pc.SDL_CreateWindow(caption, 0, 0, w, h, flags)
    if sync:
        renderer = pc.SDL_CreateRenderer(window, -1,
                                         pc.SDL_RENDERER_ACCELERATED | pc.SDL_RENDERER_PRESENTVSYNC)
    else:
        renderer = pc.SDL_CreateRenderer(window, -1, pc.SDL_RENDERER_ACCELERATED)

    if renderer is None:
        renderer = pc.SDL_CreateRenderer(window, -1, pc.SDL_RENDERER_SOFTWARE)

    return window, renderer, w, h


# View에서 가짐
class Camera:
    center = np.array([-1920 // 2, -1080 // 2 + 20])

    # idx  0:마우스, 1:키보드
    def __init__(self, idx, default_size):
        self.idx = idx
        self.pos = np.array([0.0, 0.0])
        self.default_size = default_size
        self.size = self.default_size

    def reset_size(self):
        self.size = self.default_size


class ObjM:
    '''
    objs[0] 배경
    objs[1] 오브젝
    objs[2] ui
    '''
    active_list = None

    def __init__(self):
        self.objs = [[], [], []]

    def add_object(self, o, idx=0):
        self.objs[idx].append(o)

    def remove_object(self, o):
        objects = self.objs
        for i in range(len(objects)):
            if o in objects[i]:
                objects[i].remove(o)
                del o
                break

    def clear(self):
        objects = self.objs
        for i in range(len(objects)):
            for o in objects[i]:
                del o
            objects[i].clear()

    def render(self, cam):  # Obj.그리기 루프를 통해 물체들을 그림 Camera를 전달함
        for a in self.objs:
            for b in a:
                b.render(cam)

    def tick(self, dt):
        for a in self.objs:
            for b in a:
                b.tick(dt)

    def active(self):
        ObjM.active_list = self


class View:
    # 윈도우마다 하나씩 있음
    is_first_open_canvas = True
    views = (None)
    active_view = None

    def __init__(self, idx):
        if View.is_first_open_canvas:
            win, ren, w, h = pc.open_canvas(Screen_Width, Screen_Height)
            View.is_first_open_canvas = False
        else:
            win, ren, w, h = _open_other_canvas(Screen_Width, Screen_Height)

        pc.hide_lattice()
        self.window, self.renderer = win, ren
        self.w, self.h = w, h
        self.half_w, self.half_h = w // 2, h // 2
        self.cam = Camera(idx, h / 1080)
        self.use()

    def change_scene(self):
        cam_pos = self.cam.pos
        cam_pos[0], cam_pos[1] = 0, 0

    def change_size(self, w, h):
        pc.SDL_SetWindowSize(self.window, w, h)
        self.w, self.h = w, h
        self.half_w, self.half_h = w // 2, h // 2
        self.cam.size = self.cam.default_size = h / 1080

    def use(self):
        View.active_view = self
        pc.set_window_renderer(self.window, self.renderer, self.w, self.h)

    @classmethod
    def reset(cls):
        for a in View.views:
            a.cam.pos[0] = 0
            a.cam.pos[1] = 0
            a.cam.size = a.cam.default_size


# 뷰마다 하나씩 가지기
class ImgLoader:
    def __init__(self):
        self.imgs = {}

    def load(self, path):
        if path not in self.imgs:
            self.imgs[path] = pc.load_image(path)
        return self.imgs[path]


img_loader = (ImgLoader(), ImgLoader())


# 화면 밖에 나갔는지 검사 나가면 True 반환
def is_clip(pos, size):
    hs = size // 2
    # 화면 밖에 나가면 true
    if pos[0] + hs[0] < 0 or pos[0] - hs[0] > View.active_view.w or pos[1] + hs[1] < 0 or pos[1] - hs[
        1] > View.active_view.h:
        return True
    return False


class Image:
    # DrawObj에서 호출될듯, DrawObj마다 두개씩 있음
    def load(self, path, idx):
        self.img = img_loader[idx].load(path)
        self.size = np.array([self.img.w, self.img.h])
        self.filp = False

    def render(self, pos, size):
        if is_clip(pos, size * self.size):
            return
        if self.filp:
            self.img.clip_composite_draw(0, 0, int(self.size[0]), int(self.size[1]), 0, 'h', int(pos[0]), int(pos[1]),
                                         int(size[0] * self.size[0]), int(size[1] * self.size[1]))
        else:
            self.img.draw(int(pos[0]), int(pos[1]), int(size[0] * self.size[0]), int(size[1] * self.size[1]))


TYPE_NONE, TYPE_REPEAT, TYPE_ONCE, TYPE_ONCENEXTPLAY = range(4)
ISPLAYING, ISONCEEND = range(-2, 0)


class Animation:
    # 스프라이트 시트 이미지 배치는 항상 가로로 함 나중에 애니메이션 추가시 곤란함감소
    # -애니메이션 종류: 0:none, 1:반복재생, 2:한번재생멈춤, 3:한번재생다음애니메

    def __init__(self, path, _type, sheet_count, offset):
        self.delayTime = 1 / 8.0  # 딜레이 시간 초당 재생될 프레임 8.0
        self.remainDelayTime = 0.0  # 남은 딜레이 시간

        self.imgs = []
        for i in range(len(View.views)):
            View.views[i].use()
            self.imgs.append(img_loader[i].load(path))

        self.img_width, self.img_height = self.imgs[0].w, self.imgs[0].h
        self.width, self.height = self.img_width / sheet_count, self.img_height
        self.half_width, self.half_height = self.width // 2, self.height // 2
        self.flip = ''
        self._type = _type

        self.offset = offset

        self.sheetCount = sheet_count
        self.frame = 0
        self.next_anim_idx = -1

    def play(self, next_anim_idx):  # -1이 들어오면 재생 후 종류(1,2)에 맞는 행동을 함
        self.next_anim_idx = next_anim_idx
        if self._type != 1:
            self.frame = 0
            self.remainDelayTime = 0

    def tick(self, dt):
        # TYPE_REPEAT: 한번이라도 끝나면 ISONCEEND
        # TYPE_ONCE: 끝나면 ISONCEEND
        # TYPE_ONCENEXTPLAY: 완료시 다음 idx 반환 
        if self.sheetCount == 0:
            return ISONCEEND

        self.remainDelayTime += dt
        if self.remainDelayTime > self.delayTime:
            self.remainDelayTime = 0.0
            if self._type == TYPE_ONCE:
                if self.frame + 1 == self.sheetCount:
                    return ISONCEEND
                else:
                    self.frame += 1
                    self.frame = self.frame % self.sheetCount
            elif self._type == TYPE_REPEAT:
                self.frame += 1
                self.frame = self.frame % self.sheetCount
                return ISONCEEND
            elif self._type == TYPE_ONCENEXTPLAY:
                if self.frame + 1 == self.sheetCount:
                    t = self.next_anim_idx
                    self.next_anim_idx = 0
                    self.frame = 0
                    return t
                else:
                    self.frame += 1

            assert self._type != 0

        return ISPLAYING

    def render(self, pos, size, cam):
        w = self.img_width / self.sheetCount
        tem_size = np.array([w * size[0], self.img_height * size[1]])
        tem_off = self.offset * cam.size
        tem_pos = np.array([pos[0] + tem_off[0], pos[1] + tem_off[1] + tem_size[1] // 2])
        if is_clip(tem_pos, tem_size):
            return
        if self.flip == 'h':
            tem_off[0] = -tem_off[0]
        self.imgs[cam.idx].clip_composite_draw(int(self.frame * w), 0, int(w), self.img_height,
                                               0, self.flip,
                                               int(pos[0] + tem_off[0]), int(pos[1] + tem_off[1] + tem_size[1] // 2),
                                               int(tem_size[0]), int(tem_size[1]))

    def get_size(self):
        return [self.width, self.height]

    def get_half_size(self):
        return [self.half_width, self.half_height]


class Animator:

    def __init__(self):
        self.anim_idx = 0
        self.anim_arr = []
        self.is_end = False
        self.flip = ''

    def play(self, idx, next_anim=-1):  # 두번째 전달시 종료시 자동으로 다음 애니메이션 재생
        # idx에 -1전달시 아무것도 안보임
        self.anim_idx = idx
        self.anim_arr[idx].play(next_anim)
        self.is_end = False

    # type 애니메이션 종류: 0:none, 1:반복재생, 2:한번재생멈춤, 3:한번재생다음애니메
    # TYPE_NONE, TYPE_REPEAT, TYPE_ONCE, TYPE_ONCENEXTPLAY
    def load(self, path, type, sheet_count, offset):  # 상속받을때 애니메이션들에 알맞는 이미지 넣어주기
        anim = Animation(path, type, sheet_count, offset)
        self.anim_arr.append(anim)

    # 반환값은 지금 끝난 애니메이션 인덱스
    def tick(self, dt):
        # 재생중인 애니메이션.tick(rt) 만약 0이상의 수가 반환되면
        # play(몇번째) 실행
        # 만약 실행 후 다음 애니메이션이 재생되는 거라면 다음애니메이션 재생후 지금 무슨 애니메이션 끝났는지 알려주기
        # 행동끝난뒤 실행되야하는 기능들이 있음
        animation_state = self.anim_arr[self.anim_idx].tick(dt)

        if animation_state == ISONCEEND:
            self.is_end = True
            return ISONCEEND
        elif animation_state >= 0:
            prev_idx = self.anim_idx
            self.play(animation_state)
            return prev_idx

    def render(self, pos, size, cam):
        if self.anim_idx == -1:
            return
        self.anim_arr[self.anim_idx].flip = self.flip
        self.anim_arr[self.anim_idx].render(pos, size, cam)

    def get_size(self):
        return self.anim_arr[0].get_size()


# Tick 함수가 매번 호출되는 얘들 몸통
class TickObj:

    def __init__(self, layer=0):
        self.layer = layer
        ObjM.active_list.add_object(self, self.layer)

    def tick(self, dt):  # dt deltaTime
        pass


class DrawObj(TickObj):

    def __init__(self, layer=0):
        super().__init__(layer)
        self.pos = np.array([0.0, 0.0])
        self.size = np.array([1, 1])

    def set_pos(self, x, y):
        self.pos[0], self.pos[1] = x, y

    def calculate_pos_size(self, cam):
        tem_size = self.size * np.array([cam.size, cam.size])
        tem_pos = (self.pos - cam.pos) * cam.size
        return tem_pos, tem_size

    def render(self, cam):
        # Camera (위치, 크기) 참조해서 오브젝트 그림
        # Camera 확인해서 인덱스별로 다른 이미지 그릴수 있음
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.imgs[cam.idx].render(tem_pos, tem_size)
        return tem_pos, tem_size

    def load_img(self, path):
        # 렌더러 2개라 렌더러별로 하나씩 불러줘야함.
        self.imgs = [Image() for i in range(len(View.views))]
        for i in range(len(View.views)):
            View.views[i].use()
            self.imgs[i].load(path, i)

    def load_animation(self, animation):
        pass

    def get_size(self):
        return self.imgs[0].size

    def get_halfsize(self):
        return self.imgs[0].size // 2


class TimePassDetector:
    DISABLE, CLICK, ACTIVE, START = range(4)

    def __init__(self):
        self.start(100)

    def start(self, limit_time):
        self.limitTime = limit_time
        self.state = 0
        self.elapseTime = 0.0
        self.state = TimePassDetector.START

    def cancel(self):
        if self.elapseTime < self.limitTime:
            self.state = TimePassDetector.CLICK
        else:
            self.start(100)
            self.state = TimePassDetector.DISABLE

    def check(self, dt):
        if self.state == TimePassDetector.START:
            self.elapseTime += dt
        if self.limitTime <= self.elapseTime:
            return TimePassDetector.ACTIVE
        if self.state == TimePassDetector.CLICK:
            self.state = TimePassDetector.DISABLE
            return TimePassDetector.CLICK
        return TimePassDetector.DISABLE


def mouse_pos_to_view_pos(mouse_pos, view):
    return np.array([mouse_pos[0], view.h - mouse_pos[1]])


def mouse_pos_to_world(mouse_pos, view):
    pos = mouse_pos_to_view_pos(mouse_pos, view)
    t = 1 / view.cam.size
    pos[0], pos[1] = int(pos[0] * 1 / view.cam.size), int(pos[1] * 1 / view.cam.size)
    return pos + view.cam.pos


# 키입력받는 함수에서 플레이어함수를 불러준다
class MouseController:
    pos = np.array([0, 0])
    clickTime = TimePassDetector()  # 클릭용

    is_down = False

    @classmethod
    def mouse_input(cls, x, y):
        MouseController.pos[0], MouseController.pos[1] = x, y

    @classmethod
    def interact_input(cls, isdown):  # ad, s / s키 입력중 ad가 눌리면 누르고있는동작취소
        MouseController.is_down = isdown
        if isdown:
            MouseController.clickTime.start(0.3)
        else:
            MouseController.clickTime.cancel()


class KeyController:
    x = 0
    moveTime = TimePassDetector()  # 달리기용
    is_w_down = False

    @classmethod
    def interact_input(self, isdown):  # ad, s / s키 입력중 ad가 눌리면 누르고있는동작취소
        if isdown:
            self.moveTime.start(0.3)
        else:
            self.moveTime.cancel()


def collide_rect_point(rect, point):
    if point[0] < rect[0] or rect[2] < point[0] or point[1] < rect[3] or rect[1] < point[1]:
        return False
    return True


def open_windows():
    View.views = [View(0)]
    # View.views = (View(0), View(1))


def change_scene(scene):
    import game_framework
    game_framework.change_state(scene)


def get_center():
    view = View.active_view
    return [view.half_w, view.half_h]


def change_view_size(w, h):
    for a in View.views:
        a.change_size(w, h)


def init():
    open_windows()
    load_defulat_font()


def exit():
    for a in View.views:
        a.use()
        pc.SDL_DestroyRenderer(a.renderer)
        pc.SDL_DestroyWindow(a.window)

    pc.close_canvas()
