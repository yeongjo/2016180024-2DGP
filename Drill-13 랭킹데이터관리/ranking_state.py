import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import world_build_state

name = "MainState"

def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

boy = None

def enter():
    # game world is prepared already in world_build_state
    global boy, font
    boy = world_build_state.get_boy()
    font = load_font('ENCR10B.TTF', 20)

def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world_build_state)


def update():
    for game_object in game_world.all_objects():
        game_object.update()



def draw():
    font_y = 500
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for i in range(min(10, len(game_world.ranking))):
        font.draw(30, font_y, game_world.ranking[i])
        font_y -= 50
    update_canvas()
