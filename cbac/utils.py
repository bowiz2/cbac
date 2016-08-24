from collections import namedtuple

from constants.mc_direction import UP, DOWN, NORTH, EAST, SOUTH, WEST


class Vector(namedtuple('Vector', ['x', 'y', 'z'])):
    """
    3D vector.
    """

    def __add__(self, other):

        return Vector(*[i + j for i, j in zip(self, other)])

    def __sub__(self, other):
        return Vector(*[i - j for i, j in zip(self, other)])

    def __mul__(self, other):
        return Vector(*[i * other for i in self])

    def is_adjacent(self, other):
        """
        Takes other vector and check if it is adjacent to this location.
        """
        for direction_vector in directions:
            if self == other + direction_vector:
                return True
        return False


Location = Vector


def memoize(function):
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv

    return wrapper


def format_location(location):
    return " ".join([str(i) for i in location])


def format_realtive_location(location):
    return " ".join(["~" + str(i) for i in location])


vectors = {
    UP: Vector(0, 1, 0),
    DOWN: Vector(0, -1, 0),
    NORTH: Vector(0, 0, 1),
    EAST: Vector(1, 0, 0),
    SOUTH: Vector(0, 0, -1),
    WEST: Vector(-1, 0, 0)
}