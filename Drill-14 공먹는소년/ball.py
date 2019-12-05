import game_framework
from pico2d import *
import random

import game_world


class Ball:

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('ball21x21.png')
        self.x = 0
        self.y = 0

    def get_bb(self):
        return self.x - 11, self.y - 11, self.x + 11, self.y + 11


    def set_background(self, bg):
        self.bg = bg
        self.x = random.randint(0, self.bg.w)
        self.y = random.randint(0, self.bg.h)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        pass


    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.image.draw(cx, cy)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

