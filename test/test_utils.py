"""Test the utilities which are shipped with cbac."""
from unittest import TestCase
from utils import inline_generators, _from, absolute_area


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
