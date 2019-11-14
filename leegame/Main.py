import game_framework
import PicoModule
import GamePlay



if __name__ == '__main__':
    PicoModule.init()
    state = GamePlay
    game_framework.run(state)
    PicoModule.exit()
    print("end")