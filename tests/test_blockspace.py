from unittest import TestCase

from blockspace import BlockSpace
from compound import Constant, Memory


class TestBlockSpace(TestCase):
    def test_blockspace(self):
        bs = BlockSpace((200, 200, 200))
        TEST_SIZE = 10
        for i in xrange(TEST_SIZE):
            bs.add_compound(Constant(i + 1))
            # Some bugs found.
        bs.pack()
        assert len(bs.packed_compounds) == TEST_SIZE

        bs = BlockSpace((200, 200, 200))

        MEMORY_SIZE = 8

        for i in xrange(TEST_SIZE):
            bs.add_compound(Memory(MEMORY_SIZE))
            # Some bugs found.
        self.assertEqual(len(bs.packed_blocks), MEMORY_SIZE * TEST_SIZE)
