"""
Contains all the direction string constants such as "north" and "east".
These strings are an integral part of the way minecraft represents the facing of blocks.
I chose to place them in a separate module to prevent programming error. (I typed "nprth" and did not notice.)


Also this module provide some basic functionality working with directions.
"""
UP = 'up'
DOWN = 'down'
NORTH = 'north'
EAST = 'east'
SOUTH = 'south'
WEST = 'west'


def oposite(direction):
    return {
        UP: DOWN,
        DOWN: UP,
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }[direction]

__all__ = ["UP", "DOWN", "WEST", "EAST", "SOUTH", "NORTH"]
