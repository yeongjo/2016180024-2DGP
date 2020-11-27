from PicoModule import *

fonts = []
font_idx = 0

def load_font(size = 1):
    global fonts
    for a in fonts:
        del a
    fonts = []
    fonts.append(pc.load_font("font/HoonWhitecatR.ttf", int(80 * size)))
    fonts.append(pc.load_font("font/HoonWhitecatR.ttf", int(200* size)))
    fonts.append(pc.load_font("font/HoonWhitecatR.ttf", int(400* size)))
    fonts.append(pc.load_font("font/HoonWhitecatR.ttf", int(60* size)))

def draw_text(str, pos, color=(255, 255, 255)):
    fonts[font_idx].draw(pos[0], pos[1], str, color)

def active_font(idx, is_center = False):
    global font_idx
    font_idx = idx
    fonts[font_idx].is_center = is_center