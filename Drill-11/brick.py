import game_framework
from pico2d import *

class Brick:
    def __init__(self):
        self.x, self.y = 1600 // 2, 170
        self.image = load_image('brick180x40.png')
        self.velocity = 1

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def update(self):
        self.x += self.velocity
        if self.x < 90 or 1600 - 90 < self.x:
            self.velocity = -self.velocity

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
