from collections import namedtuple


class Vector(namedtuple('Vector', ['x', 'y', 'z'])):

    def __add__(self, other):

        return Vector(*[i + j for i, j in zip(self, other)])

    def __mul__(self, other):
        return Vector(*[i * other for i in self])

Location = Vector