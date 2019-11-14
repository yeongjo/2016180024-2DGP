from PicoModule import *
from GamePlay import *

class Building(DrawObj):
    def __init__(self):
        super().__init__()
        self.load_img('img/map.png')
