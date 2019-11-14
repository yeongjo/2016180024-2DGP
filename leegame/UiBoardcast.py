from PicoModule import *
from GamePlay import *

class UiBoardcast(DrawObj):
    def __init__(self, remain_time):
        self.remain_time = remain_time
    def tick(self, dt):
