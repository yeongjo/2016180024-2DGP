import sys
import os
import types
import ctypes
import math
import json

#try:
#except ImportError:
#    print("Error: cannot import pysdl2 - probably not installed")
#    sys.exit(-1) # abort program execution




lattice_on = True
audio_on = False


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def get_canvas_width():
    return canvas_width

def get_canvas_height():
    return canvas_height


def open_canvas(w=int(800), h=int(600), sync=False, full=False):
    global canvas_width, canvas_height

    canvas_width, canvas_height = w, h
