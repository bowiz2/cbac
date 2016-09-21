import cbac.assembler
import unittest
from cbac.mc_command import factory
from cbac.block import CommandBlock


class TestAssembler(unittest.TestCase):
    def test_repeat(self):
        hello_command = factory("/say hello")
        hello_command.is_repeated = True
        my_command_block = CommandBlock(hello_command)
        cbac.assembler.adjust(my_command_block, hello_command)
        self.assertEqual(my_command_block.action, "repeat")