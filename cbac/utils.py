from collections import namedtuple


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
