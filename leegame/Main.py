import game_framework
import PicoModule
import GamePlay



if __name__ == '__main__':
    PicoModule.init()
    import GamePlay as start
    state = start
    game_framework.run(state)
    PicoModule.exit()
    print("end")