"""
Tests for the unit class. mainly unit statemtns.
"""
from unittest import TestCase
from cbac.unit import Unit
from cbac.unit.statements import *
from cbac.blockspace import BlockSpace
import cbac.assembler
from test.decorators import named_schematic


class TestUnitStatements(TestCase):
    
    def setUp(self):
        self.schematic_path = "test_schematic.schematic"
        self.block_space = BlockSpace((20, 20, 20))

    def tearDown(self):
        self.block_space.pack()
        self.block_space.shrink()
        schematic = cbac.assembler.build(self.block_space)
        schematic.saveToFile(self.schematic_path)

    @named_schematic
    def test_switch(self):

        class SubjectUnit(Unit):
            def __init__(self):
                super(SubjectUnit, self).__init__(8)
                self.input = self.create_input(8)
                self.output = self.create_output(2)
                self.synthesis()

            def main_logic_commands(self):
                yield Switch(self.input).by(
                    case[4](self.output.blocks[0].shell.activate()),
                    case[2](self.output.blocks[1].shell.activate())
                )

        self.block_space.add_unit(SubjectUnit())
