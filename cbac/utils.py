from collections import namedtuple
import types


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


def format_area(area):
    """
    ((1, 2, 3), (4, 5, 6)) --> 1 2 3 4 5 6
    :param area:
    :return:
    """
    return " ".join([format_location(point) for point in area])


def format_relative_area(area):
    """
    Format an area to the format of minecraft relative position
    aka
    ((1, 2, 3), (4, 5, 6)) --> ~1 ~2 ~3 ~4 ~5 ~6
    """
    return " ".join([format_realtive_location(point) for point in area])


def inline_generators(fn):
    """
    Used for implementing yield from in python.
    :param fn:
    :return:
    """

    def inline(value):
        if isinstance(value, InlineGenerator):
            for x in value.wrapped:
                for y in inline(x):
                    yield y
        else:
            yield value

    def wrapped(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, types.GeneratorType):
            result = inline(_from(result))
        return result

    return wrapped


class InlineGenerator(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped


def absolute_area(area):
    """
    Takes an area and converts it into absolute location
    :param area:
    :return: area
    """
    point_a, point_b = area
    point_a = Vector(*point_a)
    point_b = Vector(*point_b)
    diff = point_b - point_a
    return ((0, 0, 0), diff)


def _from(value):
    assert isinstance(value, types.GeneratorType)
    return InlineGenerator(value)
