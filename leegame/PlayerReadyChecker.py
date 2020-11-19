import Font
import TitleScene
from PicoModule import get_center
from Sound import Sound

mouseuser_ready = False
keyuser_ready = False

view_center = get_center()

def reset():
    global mouseuser_ready, keyuser_ready, pop_sound
    mouseuser_ready = False
    keyuser_ready = False
    pop_sound = Sound.load('sound/Pop.wav', 100)

def set_mouse_input():
    global mouseuser_ready
    mouseuser_ready = True
    pop_sound.play()

def set_key_input():
    global keyuser_ready
    keyuser_ready = True
    pop_sound.play()

def check_ready_status():
    return mouseuser_ready and keyuser_ready

def render_status(idx, pos = view_center):
    # if idx == 0:
    if TitleScene.isServer:
        render_mouse_status(pos)
    else:
        render_key_status(pos)

def render_mouse_status(pos = view_center):
    Font.active_font(3, True)
    if mouseuser_ready:
        Font.draw_text("마우스 준비완료!", pos)
    else:
        Font.draw_text("마우스를 눌러주세요", pos)

def render_key_status(pos = view_center):
    Font.active_font(3, True)
    if keyuser_ready:
        Font.draw_text("키보드 준비완료!", pos)
    else:
        Font.draw_text("아무 키나 눌러주세요 esc말고요", pos)
