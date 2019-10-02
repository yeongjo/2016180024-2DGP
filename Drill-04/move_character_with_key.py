from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')

running = True
dir = 1
img_dir = 1
x = 800 // 2
frame = 0

while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 100 * img_dir, 100, 100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    x += dir * 15
    if x >= 800:
        dir = -1
        img_dir = 0
    elif x <= 0:
        dir = 1
        img_dir = 1
    delay(0.03)

close_canvas()

