from pico2d import *
import random as rd
# Game object class here

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

class Boy:
    def __init__(self):
        self.x, self.y = rd.randint(100, 700),90
        self.frame = 0
        self.floatFrame = 0.0
        self.image = load_image('run_animation.png')

    def update(self):
        self.floatFrame += rd.random() + 0.5
        self.floatFrame = self.floatFrame % 8
        self.frame = int(self.floatFrame)
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

class Ball:
    def __init__(self):
        self.x, self.y = rd.randint(100, 700),599
        if rd.randint(0,2) > 1:
            self.image = load_image('ball41x41.png')
            self.h = 41//2
        else:
            self.image = load_image('ball21x21.png')
            self.h = 21//2
        self.dropSpeed = rd.random() * 4 + 2

    def update(self):

        self.y -= 5 * self.dropSpeed
        if self.y <= 50 + self.h:
            self.y = 50 + self.h

    def draw(self):
        self.image.draw(self.x, self.y)


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400,30)


# initialization code
open_canvas()
team = [Boy() for i in range(11)]
balls = [Ball() for i in range(20)]
grass = Grass()
running = True

# game main loop code
while running:
    handle_events()

    for boy in team:
        boy.update()
    for boy in balls:
        boy.update()

    clear_canvas()
    grass.draw()
    for boy in team:
        boy.draw()
    for boy in balls:
        boy.draw()
    update_canvas()

    delay(0.05)

# finalization code