import assembler
from blockspace import BlockSpace
from compound import Memory, SwitchFlow, Constant, CBA
from unittest import TestCase
from .const import SCHEMATIC_FORMAT
from constants.block_id import TRUE_BLOCK


class TestFlow(TestCase):
    """
    Tests control flow.
    """

    def test_condition(self):
        const = Constant(3)
        cba = CBA(const.blocks[0].shell == TRUE_BLOCK, "/say it is true.")
        block_space = BlockSpace((8, 8, 8), const, cba)
        schematic = assembler.build(block_space)
        schematic.saveToFile(
            SCHEMATIC_FORMAT.format(self.__class__.__name__, self.test_condition.__name__))

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
        block_space = BlockSpace((15, 20, 15), memory, *(switch.comparables + [switch]))
        schematic = assembler.build(block_space)
        schematic.saveToFile(
            SCHEMATIC_FORMAT.format(self.__class__.__name__, self.test_switch.__name__))