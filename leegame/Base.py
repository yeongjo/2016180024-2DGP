import pico2d

pico2d.open_canvas()


class ObjM:
    # 모든 오브젝가지고 tick Render 들어올때마다 루프에서 돌려줌
    # 씬별로 달라야함 다른 씬이 불려오면 다른 오브젝매니저가 불림
    objs = []

    def Render(dt):  # Obj.그리기 루프를 통해 물체들을 그림 Camera를 전달함
        pass


class Camera:
    # View에서 가짐
    pos = [0, 0]
    idx = 0  # 0:마우스, 1:키보드


class View:
    # 윈도우마다 하나씩 있음
    cam = Camera()
    # -SDL_window
    # -SDL_renderer
    objM = ObjM()

    def Render(Camera):
        pass

    def tick(self, dt):
        pass


class Scene:
    # 랜더랑 틱 함수를 메인에서 불러줘야함
    view = [View(), View()]

    def Render(self):  # View 각자의 그리기를 불러줌
        pass

    def tick(self, dt):
        pass


class TickObj:
    # 매니저 클래스들이 가짐 tick 당 호출이 필요한친구들
    def tick(dt):  # dt 프레임이 동적으로 변해서 넣음
        pass


class Image:
    pass


class DrawObj(TickObj):
    # 오브젝매니저가 가짐, 이걸상속해서 다른 오브젝트 만들어야할듯
    pos = [0, 0]
    size = [0, 0]
    img = Image()  # 그냥 이미지일수도 애니메이터일수도 있음 상속받은 오브젝트에서 결정하기

    def render(self, cam):
        # Camera (위치, 크기) 참조해서 오브젝트 그림
        # Camera 확인해서 다른 이미지를 그려야함
        # Camera 인덱스 번호읽어서 다른 플레이별로 색 다른 이미지 읽어도 좋을듯
        pass

    def load(self, path):  # init에서 불러주고 init은 __init__ 에서 불러주기로
        # 렌더러 2개라 렌더러별로 하나씩 불러줘야함.
        pass


class Image:
    # DrawObj에서 호출될듯, DrawObj마다 두개씩 있음
    def load(self):
        pass

    def render(self, pos, size):
        pass


class Animator:
    animIdx = 0
    animArr = []
    isEnd = False

    def play(self, idx, next_anim=-1):  # 두번째 전달시 종료시 자동으로 다음 애니메이션 재생
        pass

    def stop(self):  # 걷기는 언제 멈출지 모름
        pass

    def load(self):
        pass

    def tick(self, rt):  # 재생중인 애니메이션.tick(rt) 만약 0이상의 수가 반환되면
        # play(몇번째) 실행
        pass

    def __init__(self):  # 상속받을때 애니메이션들에 알맞는 이미지 넣어주기
        pass


class Animation:
    # 스프라이트 시트 이미지 배치는 항상 가로로 함 나중에 애니메이션 추가시 곤란함감소
    type = 0  # -애니메이션 종류: 0:none, 1:반복재생, 2:한번재생멈춤, 3:한번재생다음애니메
    sheetCount = 0  # -이미지의 개수
    imgIdx = 0  # -ImgIdx
    delayTime = 0  # -딜레이 시간
    remainDelayTime = 0  # -남은 딜레이 시간

    nextAnimIdx = -1  # -nextAnimIdx

    def 재생(self, nextAnimIdx):  # -1이 들어오면 재생 후 종류(1,2)에 맞는 행동을 함
        pass

    def tick(self, rt):
        # 2일땐 (imgidx def  1 == 이미지의개수) then return -1
        # 1일땐 남은 딜레이 시간 > 딜레이시간 then def def ImgIdx%이미지의개수; return -1
        # 3일땐 (imgidx def  1 == 이미지의개수) then
        # t = nextAnimIdx; nextAnimIdx = 0; return nextAnimIdx
        pass

    def render(self, pos, size):  # render에서 종류#0이면 바로 return
        pass


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


class Timer:
    pass


class TimerM:
    pass


class TimePassDetecter:
    limitTime = 0
    elapseTime = 0
    state = 0  # int 클릭이면 1, 누르고있으면 2, 암것도아니면 0

    def start(self):
        active = True

    def cancel(self):  # 중간에 취소할일있으면 눌린상태가 2에서 0으로 변경됨
        pass

    def check(self):
        # [다른곳에서 사용법] 2가 반환되면 꾹누를때하는 동작을 수행한다. 꾸준히 검사하다. 0이 나오면 취소, 혹은 경우에 따라서 이동으로 취소도 가능, 조작에서 해야함
        # [클릭 및 꾹누름 인식방식]
        # 누를때 타이머 시작, 일정이상 시간이 지났는지 검사해서 드래그로 인식하고 그전에 떼면 클릭으로 간주한다.
        pass


# 키입력받는 함수에서 플레이어함수를 불러준다
class Player1Controller:
    pos = [0, 0]
    clickTime = TimePassDetecter()  # 클릭용
    moveTime = TimePassDetecter()  # 화면이동용

    def mouseInput(self, x, y):
        pass


class Player2Controller:
    x = 0
    moveTime = TimePassDetecter()  # 화면이동용

    def moveInput(self):  # ad, s / s키 입력중 ad가 눌리면 누르고있는동작취소
        pass


# 배경그려야함

class Background(DrawObj):
    # 이미지 설정해주고 배치하기
    -이미지
