from pico2d import *


def handle_events():
    global running
    global dir
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            print('key down')
            if event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1
    pass


open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')

running = True
dir = 0
x = 800 // 2
frame = 0

while running:
    clear_canvas()
    grass.draw(400, 30)
    for y in range(1, 1000):
        character.clip_draw(frame * 100, 100 * 1, 100, 80, x, y)
    update_canvas()

    handle_events()
    frame = (frame + 1) % 8
    x += dir * 5
    print(dir)
    #delay(0.03)

close_canvas()

