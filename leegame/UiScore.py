from GamePlay import *


class UiScore(DrawObj):

    def __init__(self, name):
        super().__init__(1)
        self.name = name
        self.value = 0
        self.pos[0] = 30

    def render(self, cam):
        import Font
        Font.active_font(0)
        Font.draw_text(str(self.value) + ' ' + self.name, (self.pos[0], self.pos[1]))
