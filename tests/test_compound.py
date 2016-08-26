import random
from unittest import TestCase
import cbac.assembler as assembler
import cbac.block as block
from cbac.blockspace import BlockSpace
from cbac.compound import Compound, CBA
from cbac.compound import Register
from cbac.compound import Constant
from cbac.compound import Extender
from cbac.constants.block_id import FALSE_BLOCK
import tests.decorators


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
        memory = Register(BITS)
        self.assertEqual(len(memory.blocks), BITS)

        for i in xrange(BITS):
            self.assertEqual(memory.blocks[i].block_id, FALSE_BLOCK)

    def test_get_sub_memory(self):
        BITS = 8
        big_memory = Register(BITS)
        sub = big_memory.get_sub_memory(xrange(BITS / 2))
        self.assertIsNotNone(sub)
        self.assertEqual(len(sub.blocks), BITS / 2)

    @tests.decorators.save_schematic
    def test_extender(self):
        cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
        cba2 = CBA("/say this is totaly a new cba", "/say really.")
        ext = Extender(cba, cba2)

        block_space = BlockSpace((8, 8, 8))
        for comp in [cba, cba2, ext]:
            block_space.add(comp)

        # build a schematic and save it to file.
        return assembler.build(block_space)
