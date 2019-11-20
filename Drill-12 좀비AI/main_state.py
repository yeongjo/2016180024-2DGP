import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from ground import Ground
from zombie import Zombie
from ball import Ball


name = "MainState"

boy = None
zombie = None
balls = []


def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def distance_sqaure(a, b):
    x1, y1, x2, y2 = a.x, a.y, b.x, b.y
    return (x1 - x2)**2 + (y1 - y2)**2

def get_boy():
    return boy

def get_balls():
    return balls

def remove_ball(o):
    if o in balls:
        balls.remove(o)
        game_world.remove_object(o)


def get_collide_ball(obj):
    for a in balls:
        if collide(a, obj):
            return a
    return None

def get_min_distance_ball(obj):
    min_distance = 10000000
    min_ball = None
    for a in balls:
        tem_distance = distance_sqaure(a, obj)
        if tem_distance < min_distance:
            min_distance = tem_distance
            min_ball = a

    return min_ball, min_distance


def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global zombie
    zombie = Zombie()
    game_world.add_object(zombie, 1)

    ground = Ground()
    game_world.add_object(ground, 0)

    global balls
    balls = [Ball() for i in range(20)]
    game_world.add_objects(balls, 1)

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
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    if collide(boy, zombie):
        if boy.health < zombie.health:
            game_world.remove_object(boy)
            game_framework.quit()
        else:
            game_world.remove_object(zombie)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






