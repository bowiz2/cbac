from collections import namedtuple


class Vector(namedtuple('Vector', ['x', 'y', 'z'])):

    def __add__(self, other):
        return Vector(*[i + j for i, j in zip(self, other)])

    def __str__(self):
        return " ".join(map(str, self.__iter__()))


Location = Vector