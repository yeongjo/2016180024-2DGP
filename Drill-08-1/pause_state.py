import random
import json
import os

from pico2d import *

import game_framework
import pause_state



name = "MainState"

pause = None



class Pause:
    def __init__(self):
        self.image = load_image('pause.png')

    def draw(self):
        self.image.draw(400, 300)


def enter():
    global pause
    pause = Pause()


def exit():
    global pause
    del(pause)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN and e.key == SDLK_p:
            game_framework.pop_state()


def update():
    pass

def draw():
    clear_canvas()
    pause.draw()
    update_canvas()





