"""
Contains all the direction string constants such as "north" and "east".
These strings are an integral part of the way minecraft represents the facing of blocks.
I chose to place them in a separate module to prevent programming error. (I typed "nprth" and did not notice.)


Also this module provide some basic functionality working with directions.
"""
from cbac.core.utils import Vector


class MCDirection(object):
    UP = 'up'
    DOWN = 'down'
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'

    @staticmethod
    def opposite(direction):
        """
        Get the opposite direction
        :param direction:
        :return:
        """
        return {
            MCDirection.UP: MCDirection.DOWN,
            MCDirection.DOWN: MCDirection.UP,
            MCDirection.NORTH: MCDirection.SOUTH,
            MCDirection.SOUTH: MCDirection.NORTH,
            MCDirection.EAST: MCDirection.WEST,
            MCDirection.WEST: MCDirection.EAST
        }[direction]

    vectors = {
        UP: Vector(0, 1, 0),
        DOWN: Vector(0, -1, 0),
        NORTH: Vector(0, 0, 1),
        EAST: Vector(1, 0, 0),
        SOUTH: Vector(0, 0, -1),
        WEST: Vector(-1, 0, 0)
    }


    @staticmethod
    def from_vector(vector):
        """
        Get a direction form a vector.

        I chose to implement that because it is the simplest way.
        Premature optimisation is the root of all evil.
        """
        assert vector in MCDirection.vectors.values(), "{0} is not one of {1}".format(vector,
                                                                                      MCDirection.vectors.values())
        for direction, direction_vector in MCDirection.vectors.items():
            if direction_vector == vector:
                return direction