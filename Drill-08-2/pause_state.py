import random
import json
import os

from pico2d import *

import game_framework
import main_state



name = "MainState"

pause_img = None



class Pause:
    def __init__(self):
        self.image = load_image('pause.png')

    def draw(self):
        self.image.draw(400, 300, 100,100)


def enter():
    global pause_img
    pause_img = Pause()


def exit():
    global pause_img
    del(pause_img)


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

logo_time=0
def draw():
    global logo_time
    main_state.draw()

    if logo_time > 1:
        pause_img.draw()
        if logo_time > 2:
            logo_time = 0
    logo_time += 0.01





