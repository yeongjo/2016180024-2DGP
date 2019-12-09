import game_framework
import PicoModule
import GamePlay



PicoModule.init()
import TitleScene as start
state = start
game_framework.run(state)
PicoModule.exit()
print("end")