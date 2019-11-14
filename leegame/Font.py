from PicoModule import *

fonts = []
font_idx = 0

fonts.append(pc.load_font("font/HoonWhitecatR.ttf", 80))
fonts.append(pc.load_font("font/HoonWhitecatR.ttf", 300))
fonts.append(pc.load_font("font/HoonWhitecatR.ttf", 400))

def draw_text(str, pos, color=(255, 255, 255)):
    fonts[font_idx].draw(pos[0], pos[1], str, color)

def active_font(idx):
    global font_idx
    font_idx = idx