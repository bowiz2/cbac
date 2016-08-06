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


    def is_adjacent(self, other):
        """
        Takes other vector and check if it is adjacent to this location.
        """
        for direction_vector in directions:
            if self == other + direction_vector:
                return True
        return False
# TODO: think of something better for the adjacency.
directions =[
    Vector(0, 1, 0),
    Vector(0, -1, 0),
    Vector(0, 0, 1),
    Vector(1, 0, 0),
    Vector(0, 0, -1),
    Vector(-1, 0, 0)
]
Location = Vector


import time

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