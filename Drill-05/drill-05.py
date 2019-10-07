from pico2d import *

KPU_HEIGHT = 600
running = True
goalPos = [400, 300]
dir = 1
img_dir = 1
x = 800 // 2
y = 400 //2
frame = 0
prev = [x,y]
i = 0

mousePos = [0,0]
open_canvas()

grass = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
arrow = load_image('hand_arrow.png')

def handle_events():
    global running, i, x, y, img_dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_MOUSEBUTTONDOWN:
            t_x, t_y = event.x, KPU_HEIGHT - 1 - event.y
            goalPos[0], goalPos[1] = t_x, t_y
            prev[0], prev[1] = x, y
            if t_x - x > 0:
                img_dir = 1
            else:
                img_dir = 0
            i = 0
        if event.type == SDL_MOUSEMOTION:
            mousePos[0], mousePos[1] = event.x, KPU_HEIGHT - 1 - event.y




while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 100 * img_dir, 100, 100, x, y)
    arrow.draw(mousePos[0] + 25, mousePos[1] - 26)
    update_canvas()
    frame = (frame + 1) % 8

    if i < 1000:
        i += 3
    t = i/1000
    x = (1 - t) * prev[0] + t * goalPos[0]
    y = (1 - t) * prev[1] + t * goalPos[1]



    handle_events()

close_canvas()
