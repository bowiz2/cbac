import unittest

from cbac import assembler
from cbac.core.block import CommandBlock
from cbac.core.mc_command import factory


class TestAssembler(unittest.TestCase):
    def test_repeat(self):
        hello_command = factory("/say hello")
        hello_command.is_repeated = True
        my_command_block = CommandBlock(hello_command)
        assembler.adjust(my_command_block, hello_command)
        self.assertEqual(my_command_block.action, "repeat")
