import random
from unittest import TestCase

import assembler
import block
from blockspace import BlockSpace
from compound import Compound, Constant, Memory, CBA, Extender
from constants.block_id import FALSE_BLOCK


class TestCompound(TestCase):
    def test_base(self):
        BLOCK_LENGTH = 4

        get_random_block = lambda: block.Block(random.choice(block.ids.names.keys()))

        compound = Compound([get_random_block() for _ in xrange(BLOCK_LENGTH)])
        self.assertEqual(len(compound.blocks), BLOCK_LENGTH)

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
        memory = Memory(BITS)
        self.assertEqual(len(memory.blocks), BITS)

        for i in xrange(BITS):
            self.assertEqual(memory.blocks[i].block_id, FALSE_BLOCK)

    def test_extender(self):
        cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
        cba2 = CBA("/say this is totaly a new cba", "/say really.")
        ext = Extender(cba, cba2)

        block_space = BlockSpace((8, 8, 8), cba, cba2, ext)

        schematic = assembler.build(block_space)
