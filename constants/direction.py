from utils import Vector


UP = 'up'
DOWN = 'down'
NORTH = 'north'
EAST = 'east'
SOUTH = 'south'
WEST = 'west'

vectors = {
    UP: Vector(0, 1, 0),
    DOWN: Vector(0, -1, 0),
    NORTH: Vector(0, 0, 1),
    EAST: Vector(1, 0, 0),
    SOUTH: Vector(0, 0, -1),
    WEST: Vector(-1, 0, 0)
}

def oposite(direction):
    return {
        UP: DOWN,
        DOWN: UP,
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
     }[direction]