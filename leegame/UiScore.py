from GamePlay import *


class UiScore(DrawObj):

    def __init__(self, r, g, b):
        super().__init__(1)
        self.color = (r, g, b)
        self.value = 0

    def render(self, cam):
        draw_text(str(self.value), (10, ))
