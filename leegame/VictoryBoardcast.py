from UiBoardcast import *

class VictoryBoardcast(ImgBoardcast):
    def exit(self):
        win1 = GameManager.player1_win_count
        win2 = GameManager.player2_win_count
        #win1 = ['☆' for i in range(2-win1)]+['★' for i in range(win1)]
        #win2 = ['☆' for i in range(2-win2)]+['★' for i in range(win2)]
        ##win1_str = '♡♡'
        #text =''.join(win1) + " " + ''.join(win2)
        text =str(win1) + " " + str(win2)
        #self.pos[0] -= 300
        RoundBoardcast(text, self.pos, 2.0)

class RoundBoardcast(TextBoardcast):
    def exit(self):
        GameManager.end_boardcast()
        print("round end")

    def render(self, cam):
        off = 300
        import Font
        Font.active_font(1)
        pos = cp.copy(self.pos)
        pos[0] -= 50
        Font.draw_text('vs', pos, (230,230,230))
        Font.active_font(2)
        self.pos[0] -= off
        #Font.draw_text(self.text[0:2], self.pos, (178,27,24))
        Font.draw_text(self.text[0], self.pos, (178,27,24))
        self.pos[0] += off+off
        #Font.draw_text(self.text[3:5], self.pos, (87,227,210))
        Font.draw_text(self.text[2], self.pos, (87,227,210))
        self.pos[0] -= off

class EndVictoryBoardcast(VictoryBoardcast):
    def exit(self):
        win1 = GameManager.player1_win_count
        win2 = GameManager.player2_win_count

        text = str(win1) + " " + str(win2)
        EndRoundBoardcast(text, self.pos, 2.0)

class EndRoundBoardcast(RoundBoardcast):
    def exit(self):
        GameManager.end_boardcast()
        print("game end")