from unittest import TestCase

import cbac.assembler
from cbac.blockspace import BlockSpace
from cbac.compound import CBA
from cbac.compound import Register
from cbac.compound import Constant
from cbac.compound.switch import SwitchFlow
from cbac.constants.block_id import TRUE_BLOCK
from .decorators import save_schematic


class TestFlow(TestCase):
    """
    Tests control flow.
    """

    @save_schematic
    def test_condition(self):
        const = Constant(3)
        cba = CBA(const.blocks[0].shell == TRUE_BLOCK, "/say it is true.")
        block_space = BlockSpace((8, 8, 8))
        for c in [const, cba]:
            block_space.add(c)
        schematic = cbac.assembler.build(block_space)
        return schematic

    @save_schematic
    def test_switch(self):
        def msg(something):
            return "/say {}".format(something)

        memory = Register(8)
        # TODO: fix isolation bug.
        switch = SwitchFlow(memory, {
            Constant(0): msg("Empty :("),
            Constant(1): msg("Wow 1 is so nice."),
            Constant(2): msg("2 is so much better"),
            Constant(3): msg("3 is ruller!")
        })

        switch.isolated = True

        block_space = BlockSpace((15, 20, 15))
        for c in switch.comparables + [memory, switch]:
            block_space.add(c)

        schematic = cbac.assembler.build(block_space)
        return schematic
