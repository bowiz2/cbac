from unittest import TestCase

from cbac.core.block import BlockID

from cbac.core.compound import HardwareConstant
from cbac.core.compound import Register


class TestCompound(TestCase):
    def test_constant(self):
        NUM = 5
        const = HardwareConstant(NUM)
        self.assertEqual(const.number, NUM)

        excpected = (True, False, True, False, False, False, False, False)

        for present_item, excpected_item in zip(const.blocks, excpected):
            if excpected_item is True:
                self.assertEqual(present_item.block_id, BlockID.TRUE_BLOCK)
            elif excpected_item is False:
                self.assertEqual(present_item.block_id, BlockID.FALSE_BLOCK)

    def test_memory(self):
        BITS = 8
        memory = Register(BITS)
        self.assertEqual(len(memory.blocks), BITS)

        for i in xrange(BITS):
            self.assertEqual(memory.blocks[i].block_id, BlockID.FALSE_BLOCK)

    def test_get_sub_memory(self):
        BITS = 8
        big_memory = Register(BITS)
        sub = big_memory.slice(xrange(BITS / 2))
        self.assertIsNotNone(sub)
        self.assertEqual(len(sub.blocks), BITS / 2)
