"""Test the utilities which are shipped with cbac."""
from unittest import TestCase

from cbac.core.utils import *
from cbac.core.utils import _from


class TestUtils(TestCase):
    def test_yield_from(self):
        def some():
            """
            yield 4 numbers
            """
            for i in xrange(4):
                yield i

        @inline_generators
        def second():
            """
            used to test inline yielding
            """
            yield "a"
            yield "b"
            yield _from(some())
            yield "c"

        self.assertEqual(tuple(second()), ("a", "b", 0, 1, 2, 3, "c"))

    def test_absolute_area(self):
        non_absolute = ((2, 3, 4), (5, 5, 5))
        self.assertEquals(absolute_area(non_absolute), ((0, 0, 0), (3, 2, 1)))

    def test_flatten(self):
        start = [(1, 2, 3), 4, 5, (6, 7), (8, (9, 10), 11)]
        result = flatten(start, 2)
        self.assertTrue(compare(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))


class TestLocations(TestCase):
    def setUp(self):
        self.a = Vector(3, 5, 1)
        self.b = Vector(1, 2, 3)
        self.c = Vector(4, 4, 4)

    def test_sort_locations(self):
        sort_x, sort_y, sort_z = sort_locations([self.a, self.b, self.c])
        self.assertEquals(sort_x[0], self.b)
        self.assertEquals(sort_x[1], self.a)
        self.assertEquals(sort_x[2], self.c)

        self.assertEquals(sort_y[0], self.b)
        self.assertEquals(sort_y[1], self.c)
        self.assertEquals(sort_y[2], self.a)

        self.assertEquals(sort_z[0], self.a)
        self.assertEquals(sort_z[1], self.b)
        self.assertEquals(sort_z[2], self.c)

    def test_min_box(self):
        self.assertEquals(min_corner([self.a, self.b, self.c]), Vector(1, 2, 1))

    def test_max_box(self):
        self.assertEquals(max_corner([self.a, self.b, self.c]), Vector(4, 5, 4))
