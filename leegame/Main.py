import game_framework
import PicoModule
import GamePlay

PicoModule.init()
import TitleScene as start
game_framework.run(start)
PicoModule.exit()
print("end")