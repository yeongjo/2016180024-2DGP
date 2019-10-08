# Load Image함수에도 랜더러받는게 있어서 개고생했다 ㅠ

import os
import copy
from pico2d import pico2d

pico2d.open_canvas()

class MWin:
    def __init__(self):
        self.window = pico2d.window
        self.renderer = pico2d.renderer
        self.h = pico2d.canvas_height
        self.w = pico2d.canvas_width
        print(1)

    def use(self):
        pico2d.window = self.window
        pico2d.renderer = self.renderer
        pico2d.canvas_height = self.h
        pico2d.canvas_width = self.w
# class MWin:
#     def __init__(self):
#         self.window = copy.copy(pico2d.window)
#         self.renderer = copy.copy(pico2d.renderer)
#         self.h = copy.copy(pico2d.canvas_height)
#         self.w = copy.copy(pico2d.canvas_width)
#
#     def use(self):
#         pico2d.window = copy.copy(self.window)
#         pico2d.renderer = copy.copy(self.renderer)
#         pico2d.canvas_height = copy.copy(self.h)
#         pico2d.canvas_width = copy.copy(self.w)


def open_canvas(w=int(800), h=int(600), sync=False, full=False):
    # SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 0);
    caption = ('Pico2D 2 (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')
    if full:
        flags = pico2d.SDL_WINDOW_FULLSCREEN
    else:
        flags = pico2d.SDL_WINDOW_SHOWN

    #window = pico2d.SDL_CreateWindow(caption, pico2d.SDL_WINDOWPOS_UNDEFINED, pico2d.SDL_WINDOWPOS_UNDEFINED, w, h,
    #                                 flags)
    window = pico2d.SDL_CreateWindow(caption, 0, 30, w, h,
                                     flags)
    if sync:
        renderer = pico2d.SDL_CreateRenderer(window, -1,
                                             pico2d.SDL_RENDERER_ACCELERATED | pico2d.SDL_RENDERER_PRESENTVSYNC)
    else:
        renderer = pico2d.SDL_CreateRenderer(window, -1, pico2d.SDL_RENDERER_ACCELERATED)

    if renderer is None:
        renderer = pico2d.SDL_CreateRenderer(window, -1, pico2d.SDL_RENDERER_SOFTWARE)

    pico2d.window = window
    pico2d.renderer = renderer
    pico2d.canvas_height = h
    pico2d.canvas_width = w
    aa = MWin()

    pico2d.clear_canvas()
    pico2d.update_canvas()
    pico2d.clear_canvas()
    pico2d.update_canvas()

    return aa

win_main = MWin()
win1 = open_canvas()

img1 = pico2d.load_image("a.png")

if pico2d.renderer is win1.renderer:
    print("win1 same")

for x in range(1,5):
    for y in range(1, 5):
        img1.draw_now(x * 100, y*100)

win_main.use()
img2 = pico2d.load_image("a.png")
for x in range(4,7):
    for y in range(4, 7):
        img2.draw_now(x * 100, y*100, 500,500)
#pico2d.renderer = win_main.renderer
win1.use()

for x in range(5,7):
    for y in range(5, 7):
        img1.draw_now(x * 100, y*100)

pico2d.delay(3)

# 첨엔 함수마다 매개변수만 추가해서 하려했는데 너무 지저분한거같아서 묶어주려고
# 클래스로 만드려했다 그런데 또 생각해보니
# 전역변수만 쓸때마다 교체해주면 되는거였다. Opengl 처럼럼
# class mPico:
#     def open_canvas(self, w=int(800), h=int(600), sync=False, full=False):
#         self.window, self.renderer
#         self.canvas_width, self.canvas_height
#
#         self.canvas_width, self.canvas_height = w, h
#
#         #SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 0);
#         caption = ('Pico2D Canvas (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')
#         if full:
#             flags = SDL_WINDOW_FULLSCREEN
#         else:
#             flags = SDL_WINDOW_SHOWN
#
#         self.window = SDL_CreateWindow(caption, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, w, h, flags)
#         if sync:
#             self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
#         else:
#             self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
#
#         if self.renderer is None:
#             self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_SOFTWARE)
#
#         clear_canvas(self.renderer)
#         update_canvas(self.renderer)
#         clear_canvas(self.renderer)
#         update_canvas(self.renderer)
#
#         return self.renderer
#
#     def clear_canvas(self):
#         SDL_SetRenderDrawColor(self.renderer, 200, 200, 210, 255)
#         SDL_RenderClear(self.renderer)
#         if lattice_on:
#             SDL_SetRenderDrawColor(self.renderer, 180, 180, 180, 255)
#             for x in range(0, self.canvas_width, 10):
#                 SDL_RenderDrawLine(self.renderer, x, 0, x, self.canvas_height)
#             for y in range(self.canvas_height-1, 0, -10):
#                 SDL_RenderDrawLine(self.renderer, 0, y, self.canvas_width, y)
#             SDL_SetRenderDrawColor(self.renderer, 160, 160, 160, 255)
#
#             for x in range(0, self.canvas_width, 100):
#                 SDL_RenderDrawLine(self.renderer, x, 0, x, self.canvas_height)
#             for y in range(self.canvas_height-1, 0, -100):
#                 SDL_RenderDrawLine(self.renderer, 0, y, self.canvas_width, y)
#
#     def update_canvas(self):
#         SDL_RenderPresent(self.renderer)
#
#     def clear_canvas(self):
#         SDL_SetRenderDrawColor(self.renderer, 200, 200, 210, 255)
#         SDL_RenderClear(self.renderer)
#         if lattice_on:
#             SDL_SetRenderDrawColor(self.renderer, 180, 180, 180, 255)
#             for x in range(0, self.canvas_width, 10):
#                 SDL_RenderDrawLine(self.renderer, x, 0, x, self.canvas_height)
#             for y in range(self.canvas_height-1, 0, -10):
#                 SDL_RenderDrawLine(self.renderer, 0, y, self.canvas_width, y)
#             SDL_SetRenderDrawColor(self.renderer, 160, 160, 160, 255)
#
#             for x in range(0, self.canvas_width, 100):
#                 SDL_RenderDrawLine(self.renderer, x, 0, x, self.canvas_height)
#             for y in range(self.canvas_height-1, 0, -100):
#                 SDL_RenderDrawLine(self.renderer, 0, y, self.canvas_width, y)
#
#     def resize_canvas(self,w, h):
#         self.canvas_width, self.canvas_height = w, h
#         SDL_SetWindowSize(self.window, w, h)
#         caption = ('Pico2D Canvas (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')
#         SDL_SetWindowTitle(self.window, caption)
#         clear_canvas_now()
#
#     def clear_canvas_now(self):
#         clear_canvas()
#         update_canvas()
#         clear_canvas()
#         update_canvas()
#
#     def set_renderer(self):
#         pico2d.renderer = self.renderer
#
# class Image:
#     """Pico2D Image Class"""
#
#     def __init__(self, texture):
#         self.texture = texture
#         # http://wiki.libsdl.org/SDL_QueryTexture
#         w, h = c_int(), c_int()
#         SDL_QueryTexture(self.texture, None, None, ctypes.byref(w), ctypes.byref(h))
#         self.w, self.h = w.value, h.value
#
#     def __del__(self):
#         SDL_DestroyTexture(self.texture)
#
#     def rotate_draw(self, renderer, rad, x, y, w = None, h = None):
#         """Rotate(in radian unit) and draw image to back buffer, center of rotation is the image center"""
#         if w == None and h == None:
#             w,h = self.w, self.h
#         rect = to_sdl_rect(x-w/2, y-h/2, w, h)
#         SDL_RenderCopyEx(renderer, self.texture, None, rect, math.degrees(-rad), None, SDL_FLIP_NONE)
#
#     def composite_draw(self, renderer, rad, flip, x, y, w = None, h = None):
#         if w is None and h is None:
#             w,h = self.w, self.h
#         rect = to_sdl_rect(x-w/2, y-h/2, w, h)
#         flip_flag = SDL_FLIP_NONE
#         if 'h' in flip:
#             flip_flag |= SDL_FLIP_HORIZONTAL
#         if 'v' in flip:
#             flip_flag |= SDL_FLIP_VERTICAL
#         SDL_RenderCopyEx(renderer, self.texture, None, rect, math.degrees(-rad), None, flip_flag)
#
#     def draw(self, renderer, x, y, w=None, h=None):
#         """Draw image to back buffer"""
#         if w == None and h == None:
#             w,h = self.w, self.h
#         rect = to_sdl_rect(x-w/2, y-h/2, w, h)
#         SDL_RenderCopy(renderer, self.texture, None, rect)
#
#     def draw_to_origin(self, renderer, x, y, w=None, h=None):
#         """Draw image to back buffer"""
#         if w == None and h == None:
#             w,h = self.w, self.h
#         rect = to_sdl_rect(x, y, w, h)
#         SDL_RenderCopy(renderer, self.texture, None, rect)
#
#     def clip_draw(self, left, bottom, width, height, x, y, w=None, h=None):
#         """Clip a rectangle from image and draw"""
#         if w == None and h == None:
#             w,h = width, height
#         src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
#         dest_rect = to_sdl_rect(x-w/2, y-h/2, w, h)
#         SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect)
#
#     def clip_composite_draw(self, left, bottom, width, height, rad, flip, x, y, w = None, h = None):
#         if w is None and h is None:
#             w,h = self.w, self.h
#         src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
#         dst_rect = to_sdl_rect(x-w/2, y-h/2, w, h)
#         flip_flag = SDL_FLIP_NONE
#         if 'h' in flip:
#             flip_flag |= SDL_FLIP_HORIZONTAL
#         if 'v' in flip:
#             flip_flag |= SDL_FLIP_VERTICAL
#         SDL_RenderCopyEx(renderer, self.texture, src_rect, dst_rect, math.degrees(-rad), None, flip_flag)
#
#     def clip_draw_to_origin(self, left, bottom, width, height, x, y, w=None, h=None):
#         """Clip a rectangle from image and draw"""
#         if w == None and h == None:
#             w,h = width, height
#         src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
#         dest_rect = to_sdl_rect(x, y, w, h)
#         SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect)
#
#
#     def draw_now(self, x, y, w=None, h=None):
#         """Draw image to canvas immediately"""
#         self.draw(x,y,w,h)
#         update_canvas()
#         self.draw(x,y,w,h)
#         update_canvas()
#         '''
#         if w == None and h == None:
#             w,h = self.w, self.h
#         rect = to_sdl_rect(x-w/2, y-h/2, w, h)
#         SDL_RenderCopy(renderer, self.texture, None, rect);
#         SDL_RenderPresent(renderer)
#         '''
#
#     def opacify(self, o):
#         SDL_SetTextureAlphaMod(self.texture, int(o*255.0))
#
#     def clip_image(self, left, bottom, width, height):
#         clip_texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, width, height)
#         SDL_SetRenderTarget(renderer, clip_texture)
#         SDL_RenderClear(renderer)
#         src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
#         SDL_RenderCopy(renderer, self.texture, src_rect, None)
#         SDL_SetRenderTarget(renderer, None)
#         return Image(clip_texture)
