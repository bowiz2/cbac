import random
from unittest import TestCase

import cbac.block as block
from cbac.compound import Constant
from cbac.compound import Register
from cbac.constants.block_id import FALSE_BLOCK


class TestCompound(TestCase):
    def test_constant(self):
        NUM = 5
        const = Constant(NUM)
        self.assertEqual(const.number, NUM)

        excpected = (True, False, True, False, False, False, False, False)

        for present_item, excpected_item in zip(const.blocks, excpected):
            if excpected_item is True:
                self.assertEqual(present_item.block_id, block.ids.TRUE_BLOCK)
            elif excpected_item is False:
                self.assertEqual(present_item.block_id, block.ids.FALSE_BLOCK)

    def test_memory(self):
        BITS = 8
        memory = Register(BITS)
        self.assertEqual(len(memory.blocks), BITS)

        for i in xrange(BITS):
            self.assertEqual(memory.blocks[i].block_id, FALSE_BLOCK)

    def test_get_sub_memory(self):
        BITS = 8
        big_memory = Register(BITS)
        sub = big_memory.slice(xrange(BITS / 2))
        self.assertIsNotNone(sub)
        self.assertEqual(len(sub.blocks), BITS / 2)
