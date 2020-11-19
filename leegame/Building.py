from PicoModule import *
from GamePlay import *
from Stair import Stair

MAP_WIDTH = 1920
MAP_HEIGHT = 1080
MAP_HALF_WIDTH = MAP_WIDTH // 2
MAP_HALF_HEIGHT = MAP_HEIGHT // 2
EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING = (218, -139, -500)

class Building(DrawObj):
    buildings = []
    stairs = []

    def __init__(self):
        super().__init__()
        self.load_img('img/map.png')

    @classmethod
    def create_buildings(cls):
        cls.buildings = []
        building_pos = [[0, MAP_HEIGHT], [MAP_WIDTH - 1, MAP_HEIGHT], [0, 0], [MAP_WIDTH - 1, 0]]
        stair_pos_x = (649, 540)
        i = 0

        while i < 4:
            cls.buildings.append(Building())
            cls.buildings[i].pos = np.array(building_pos[i])
            is_right = i % 2
            if is_right == 1:
                for img in cls.buildings[i].imgs:
                    img.filp = True
            for y in EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING:
                stair = Stair()
                stair.set_pos(-stair_pos_x[0] + 18 * is_right + cls.buildings[i].pos[0], y + cls.buildings[i].pos[1])
                Building.stairs.append(stair)
            for y in EACH_FLOOR_HEIGHT_OFFSET_PER_BUILDING:
                stair = Stair()
                stair.set_pos(stair_pos_x[1] + 18 * is_right + cls.buildings[i].pos[0], y + cls.buildings[i].pos[1])
                Building.stairs.append(stair)
                for img in stair.imgs:
                    img.filp = True
            i += 1

        for i in range(3):
            Building.stairs[i + 3].other_stair = Building.stairs[i + 6]
            Building.stairs[i + 6].other_stair = Building.stairs[i + 3]
            Building.stairs[i + 3 + 12].other_stair = Building.stairs[i + 6 + 12]
            Building.stairs[i + 6 + 12].other_stair = Building.stairs[i + 3 + 12]
