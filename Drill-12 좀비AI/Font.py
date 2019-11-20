import pico2d
import os

debug_font_path = os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF'

font = pico2d.load_font(debug_font_path, 16)
def debug_print(str, x1, y1):
    global font
    if font is not None:
        font.draw(x1, y1+50, str, (0,255,0))