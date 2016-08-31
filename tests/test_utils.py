from unittest import TestCase
from utils import inline_generators, _from


class TestUtils(TestCase):
    def test_yield_from(self):
        def some():
            for i in xrange(4):
                yield i

        @inline_generators
        def second():
            yield "a"
            yield "b"
            yield _from(some())
            yield "c"

        self.assertEqual(tuple(second()), ("a", "b", 0, 1, 2, 3, "c"))
