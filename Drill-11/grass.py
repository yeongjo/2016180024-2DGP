from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
        self.x, self.y = 700, 30

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 1000, self.y - 30, self.x + 1000, self.y + 30
