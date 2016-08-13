from unittest import TestCase

import assembler
from blockspace import BlockSpace
from unit import ReverseUnit, NotUnit, AndUnit, OrUnit, ShiftUnit, IncrementUnit, CallbackUnit
from .decorators import save_schematic


class TestUnit(TestCase):
    @staticmethod
    def sample_schematic(unit_class, size, blockspace_size=(30, 10, 30)):
        u = unit_class(size)
        block_space = BlockSpace(blockspace_size)
        block_space.add_compounds(u.compounds)
        schematic = assembler.build(block_space)
        return schematic

    @save_schematic
    def test_or(self):
        return self.sample_schematic(OrUnit, 4)

    @save_schematic
    def test_not(self):
        return self.sample_schematic(NotUnit, 4)

    @save_schematic
    def test_reverse(self):
        return self.sample_schematic(ReverseUnit, 4)

    @save_schematic
    def test_and(self):
        return self.sample_schematic(AndUnit, 4)

    @save_schematic
    def test_shift(self):
        u = ShiftUnit(8)
        block_space = BlockSpace((30, 10, 30))
        block_space.add_compounds(u.compounds)
        cb = u.entry_point.blocks[9]

        command = cb.command
        context = command.command_shell.context
        context.executor = cb
        context.blockspace = block_space
        cmd_text = command()
        self.assertEqual(cmd_text, '/fill ~-9 ~0 ~-4 ~-2 ~0 ~-4 snow 0 replace air 0')
        schematic = assembler.build(block_space)

        return schematic

    @save_schematic
    def test_incrament(self):
        return self.sample_schematic(IncrementUnit, 4, (100, 100, 100))
    @save_schematic
    def test_callback(self):
        return self.sample_schematic(CallbackUnit, 4)