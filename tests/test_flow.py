from unittest import TestCase

import assembler
from blockspace import BlockSpace
from compound import Memory, SwitchFlow, Constant, CBA
from constants.block_id import TRUE_BLOCK
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
        block_space.add_compounds([const, cba])
        schematic = assembler.build(block_space)
        return schematic

    @save_schematic
    def test_switch(self):
        def msg(something):
            return "/say {}".format(something)

        memory = Memory(8)
        # TODO: fix isolation bug.
        switch = SwitchFlow(memory, {
            Constant(0): msg("Empty :("),
            Constant(1): msg("Wow 1 is so nice."),
            Constant(2): msg("2 is so much better"),
            Constant(3): msg("3 is ruller!")
        })

        switch.isolated = True

        block_space = BlockSpace((15, 20, 15))
        block_space.add_compounds(switch.comparables + [memory, switch])

        schematic = assembler.build(block_space)
        return schematic
