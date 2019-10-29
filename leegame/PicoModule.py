import pico2d as pc
import numpy as np
import os

is_debug = False
path = "font/HoonWhitecatR.ttf"

active_view = None



def init_text():
    global font01
    font01 = pc.load_font(path, 20)


def debug_text(str, pos, color=(0, 200, 0)):
    if (is_debug):
        draw_text(str, pos, color)


def draw_text(str, pos, color=(255, 255, 255)):
    global font01
    font01.draw(pos[0], pos[1], str, color)


def open_other_canvas(w=int(800), h=int(600), sync=True, full=False):
    # SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 0);
    caption = ('Pico2D 2 (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')
    if full:
        flags = pc.SDL_WINDOW_FULLSCREEN
    else:
        flags = pc.SDL_WINDOW_SHOWN

    # window = pc.SDL_CreateWindow(caption, pc.SDL_WINDOWPOS_UNDEFINED, pc.SDL_WINDOWPOS_UNDEFINED, w, h,
    #                                 flags)
    window = pc.SDL_CreateWindow(caption, 0, 30, w, h,
                                 flags)
    if sync:
        renderer = pc.SDL_CreateRenderer(window, -1,
                                         pc.SDL_RENDERER_ACCELERATED | pc.SDL_RENDERER_PRESENTVSYNC)
    else:
        renderer = pc.SDL_CreateRenderer(window, -1, pc.SDL_RENDERER_ACCELERATED)

    if renderer is None:
        renderer = pc.SDL_CreateRenderer(window, -1, pc.SDL_RENDERER_SOFTWARE)

    pc.window = window
    pc.renderer = renderer
    pc.canvas_height = h
    pc.canvas_width = w

    # pc.set_window_renderer(window, renderer)

    pc.clear_canvas()
    pc.update_canvas()

    return window, renderer, w, h


class Camera:
    # View에서 가짐

    size = 1.0

    # idx # 0:마우스, 1:키보드

    def __init__(self, idx):
        self.idx = idx
        self.pos = np.array([0.0, 0.0])


class ObjM:
    # 모든 오브젝가지고 tick Render 들어올때마다 루프에서 돌려줌
    # 씬별로 달라야함 다른 씬이 불려오면 다른 오브젝매니저가 불림
    objs = []

    def render(self, cam):  # Obj.그리기 루프를 통해 물체들을 그림 Camera를 전달함
        for a in self.objs:
            a.render(cam)

    def tick(self, dt):
        for a in self.objs:
            a.tick(dt)


class Scene:
    # 랜더랑 틱 함수를 메인에서 불러줘야함
    objM = ObjM()

    def render(self, cam):
        self.objM.render(cam)

    def tick(self, dt):
        self.objM.tick(dt)


isFirstOpenCanvas = True


class View:
    # 윈도우마다 하나씩 있음
    # -cam
    # -SDL_window
    # -SDL_renderer

    def __init__(self, idx, scene):
        global isFirstOpenCanvas
        self.scene = scene
        if isFirstOpenCanvas:
            win, ren, w, h = pc.open_canvas(1920, 1050)
            isFirstOpenCanvas = False
        else:
            win, ren, w, h = open_other_canvas(1920, 1050)
        pc.hide_lattice()
        self.window = win
        self.renderer = ren
        self.h = h
        self.w = w
        self.cam = Camera(idx)

    def change_scene(self, scene):
        self.scene = scene

    def use(self):
        global active_view
        active_view = self
        pc.set_window_renderer(self.window, self.renderer, self.w, self.h)
        pc.canvas_height = self.w, self.h

    def render(self):
        self.use()
        self.scene.render(self.cam)
        pc.update_canvas()
        pc.clear_canvas()

    def tick(self, dt):
        self.scene.tick(dt)


# 뷰마다 하나씩 가지기
class ImgLoader:
    def __init__(self):
        self.imgs = {}

    def load(self, path):
        if path not in self.imgs:
            self.imgs[path] = pc.load_image(path)
        return self.imgs[path]

img_loader = (ImgLoader(), ImgLoader())


def is_clip(pos, size):
    hs = size // 2
    # 화면 밖에 나가면 true
    if pos[0] + hs[0] < 0 or pos[0] - hs[0] > active_view.w or pos[1] + hs[1] < 0 or pos[1] - hs[1] > active_view.h:
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
                                         int(size[0]*self.size[0]), int(size[1]*self.size[1]))
        else:
            self.img.draw(int(pos[0]), int(pos[1]), int(size[0]*self.size[0]), int(size[1]*self.size[1]))


class Animation:
    # 스프라이트 시트 이미지 배치는 항상 가로로 함 나중에 애니메이션 추가시 곤란함감소
    # -애니메이션 종류: 0:none, 1:반복재생, 2:한번재생멈춤, 3:한번재생다음애니메
    # -이미지의 개수
    # -ImgIdx

    # -nextAnimIdx

    def __init__(self):
        self.delayTime = 1 / 8.0  # -딜레이 시간
        self.remainDelayTime = 0.0  # -남은 딜레이 시간

    def load(self, path, _type, sheet_count, views, offset):
        self.imgs = [0, 0]
        views[0].use()
        self.imgs[0] = img_loader[0].load(path)
        views[1].use()
        self.imgs[1] = img_loader[1].load(path)
        self.size = np.array([self.imgs[0].w, self.imgs[0].h])
        self.flip = ''
        self._type = _type
        self.sheetCount = sheet_count
        self.offset = offset
        self.imgIdx = 0
        self.nextAnimIdx = -1

    def play(self, nextAnimIdx):  # -1이 들어오면 재생 후 종류(1,2)에 맞는 행동을 함
        self.nextAnimIdx = nextAnimIdx
        if self._type != 1:
            self.imgIdx = 0
            self.remainDelayTime = 0

    def tick(self, dt):
        # 2일땐 (imgIdx def  1 == 이미지의개수) then return -1
        # 1일땐 남은 딜레이 시간 > 딜레이시간 then def def ImgIdx%이미지의개수; return -1
        # 3일땐 (imgIdx def  1 == 이미지의개수) then
        # t = nextAnimIdx; nextAnimIdx = 0; return nextAnimIdx
        if self.sheetCount == 0:
            return -1
        self.remainDelayTime += dt
        if self.remainDelayTime > self.delayTime:
            self.remainDelayTime = 0.0
            if self._type == 2:
                if self.imgIdx + 1 == self.sheetCount:
                    return -1
                else:
                    self.imgIdx += 1
                    self.imgIdx = self.imgIdx % self.sheetCount
            elif self._type == 1:
                self.imgIdx += 1
                self.imgIdx = self.imgIdx % self.sheetCount
                return -1
            elif self._type == 3:
                if self.imgIdx + 1 == self.sheetCount:
                    t = self.nextAnimIdx
                    self.nextAnimIdx = 0
                    self.imgIdx = 0
                    return t
                else:
                    self.imgIdx += 1

            assert self._type != 0

        return -2

    def render(self, pos, size, cam):  # render에서 종류#0이면 바로 return
        w = self.size[0] / self.sheetCount
        tem_size = np.array([w * size[0], self.size[1] * size[1]])
        tem_off = self.offset * cam.size
        if is_clip(np.array([pos[0] + tem_off[0], pos[1] + tem_off[1] + tem_size[1] // 2]), tem_size):
            return
        if self.flip == 'h':
            tem_off[0] = -tem_off[0]
        self.imgs[cam.idx].clip_composite_draw(int(self.imgIdx * w), 0, int(w), self.size[1], 0, self.flip,
                                               int(pos[0] + tem_off[0]), int(pos[1] + tem_off[1] + tem_size[1] // 2),
                                               int(tem_size[0]), int(tem_size[1]))

    def get_size(self):
        return [self.size[0] / self.sheetCount, self.size[1]]


class Animator:

    def __init__(self):
        self.animIdx = 0
        self.animArr = []
        self.isEnd = False
        self.flip = ''

    def play(self, idx, next_anim=-1):  # 두번째 전달시 종료시 자동으로 다음 애니메이션 재생
        # idx에 -1전달시 아무것도 안보임
        self.animIdx = idx
        self.animArr[idx].play(next_anim)
        self.isEnd = False

    # type 애니메이션 종류: 0:none, 1:반복재생, 2:한번재생멈춤, 3:한번재생다음애니메
    def load(self, path, type, sheet_count, views, offset):  # 상속받을때 애니메이션들에 알맞는 이미지 넣어주기
        anim = Animation()
        anim.load(path, type, sheet_count, views, offset)
        self.animArr.append(anim)

    # 반환값은 지금 끝난 애니메이션 인덱스
    def tick(self, dt):
        # 재생중인 애니메이션.tick(rt) 만약 0이상의 수가 반환되면
        # play(몇번째) 실행
        # 만약 실행 후 다음 애니메이션이 재생되는 거라면 다음애니메이션 재생후 지금 무슨 애니메이션 끝났는지 알려주기
        # 행동끝난뒤 실행되야하는 기능들이 있음
        _idx = self.animArr[self.animIdx].tick(dt)

        if _idx == -1:
            self.isEnd = True
        elif _idx >= 0:
            prev_idx = self.animIdx
            self.play(_idx)
            return prev_idx
        return -1

    def render(self, pos, size, cam):
        if self.animIdx == -1:
            return
        self.animArr[self.animIdx].flip = self.flip
        self.animArr[self.animIdx].render(pos, size, cam)

    def get_size(self):
        return self.animArr[0].get_size()


# 매개변수 하나만 (다른거 실행중에도 바로 넘어가야한다)
# 걷기, 멈추기, 뛰기 : 상태가 참일때 반복재생, Input에 x값이 변할때만 재생시킴
# 쓰러지기(2개) : 한번재생 끝
# 상호작용들 : 한번재생되고 마무리될때 이벤트 호출
# 두명에서 상호작용하는것들이 있어서 그 때만 아무것도 안보이게하는거도 필요함

# 잠깐 기능 적음
#
# ad
# s 꾹누르면 달리기
# 짧게 누르면 상호작용
#
# 마우스 이동 화면 외곽에서 오래 있으면 그곳으로 화면이 넘어간다.
# 좌클릭 오래 누르는 동작시 공격
# 짧게 누를시 상호작용 버튼 끌때 필요함

class TickObj:
    # 매니저 클래스들이 가짐 tick 당 호출이 필요한친구들
    def __init__(self, objM):
        objM.objs.append(self)

    def tick(self, dt):  # dt deltaTime
        pass


class DrawObj(TickObj):
    # 오브젝매니저가 가짐, 이걸상속해서 다른 오브젝트 만들어야할듯

    # imgs = [Image(),Image()]  # 그냥 이미지일수도 애니메이터일수도 있음 상속받은 오브젝트에서 결정하기

    def __init__(self, objm):
        super().__init__(objm)
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
        # Camera 확인해서 다른 이미지를 그려야함
        # Camera 인덱스 번호읽어서 다른 플레이별로 색 다른 이미지 읽어도 좋을듯
        tem_pos, tem_size = self.calculate_pos_size(cam)
        self.imgs[cam.idx].render(tem_pos, tem_size)
        return tem_pos, tem_size

    def load_img(self, path, views):  # init에서 불러주고 init은 __init__ 에서 불러주기로
        # 렌더러 2개라 렌더러별로 하나씩 불러줘야함.
        self.imgs = [Image(), Image()]
        views[0].use()
        self.imgs[0].load(path, 0)
        views[1].use()
        self.imgs[1].load(path, 1)
        #self.size = self.imgs[0].size

    def load_animation(self, animation):
        pass


class TimePassDetecter:
    limitTime = 0.0
    elapseTime = 0.0
    state = -1  # int 클릭이면 1, 누르고있으면 2, 암것도아니면 -1, 시작하고 누른거면 0

    def start(self, limitTime):
        self.state = 0
        self.limitTime = limitTime

    def cancel(self):  # 중간에 취소할일있으면 눌린상태가 2에서 0으로 변경됨
        if self.state == 0:
            if self.elapseTime < self.limitTime:
                self.elapseTime = 0.0
                self.state = 1

        elif self.state == 2:
            if self.elapseTime > self.limitTime:
                self.elapseTime = 0.0
                self.state = -1

    def check(self, dt):
        # [다른곳에서 사용법] 2가 반환되면 꾹누를때하는 동작을 수행한다. 꾸준히 검사하다. 0이 나오면 취소, 혹은 경우에 따라서 이동으로 취소도 가능, 조작에서 해야함
        # [클릭 및 꾹누름 인식방식]
        # 누를때 타이머 시작, 일정이상 시간이 지났는지 검사해서 드래그로 인식하고 그전에 떼면 클릭으로 간주한다.
        if self.state == -1:
            return -1
        self.elapseTime += dt
        if self.state == 1:
            self.state = -1
            return 1
        if self.elapseTime > self.limitTime:
            self.state = 2
            return 2


def mouse_pos_to_view_pos(mouse_pos, view):
    return np.array([mouse_pos[0], view.h - mouse_pos[1]])


def mouse_pos_to_world(mouse_pos, view):
    pos = mouse_pos_to_view_pos(mouse_pos, view)
    t = 1 / view.cam.size
    pos[0], pos[1] = int(pos[0] * 1 / view.cam.size), int(pos[1] * 1 / view.cam.size)
    return pos + view.cam.pos


# 키입력받는 함수에서 플레이어함수를 불러준다
class Player1Controller:
    pos = np.array([0, 0])
    clickTime = TimePassDetecter()  # 클릭용
    # moveTime = TimePassDetecter()  # 화면이동용

    is_down = False

    def mouseInput(self, x, y):
        Player1Controller.pos[0], Player1Controller.pos[1] = x, y

    def interact_input(self, isdown):  # ad, s / s키 입력중 ad가 눌리면 누르고있는동작취소
        Player1Controller.is_down = isdown
        if isdown:
            Player1Controller.clickTime.start(0.3)
        else:
            Player1Controller.clickTime.cancel()


class Player2Controller:
    x = 0
    moveTime = TimePassDetecter()  # 달리기용

    def interact_input(self, isdown):  # ad, s / s키 입력중 ad가 눌리면 누르고있는동작취소
        if isdown:
            self.moveTime.start(0.3)
        else:
            self.moveTime.cancel()


def check_coll_rect(rect, point):
    if point[0] < rect[0] or rect[2] < point[0] or point[1] < rect[3] or rect[1] < point[1]:
        return False
    return True
