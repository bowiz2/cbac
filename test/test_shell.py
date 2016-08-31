from unittest import TestCase
from cbac.block import Block, CommandBlock
from cbac.command_shell import LocationShell, ShellContext, CommandShell
from cbac.blockspace import BlockSpace
from cbac.utils import Vector, memoize
from cbac.constants.block_id import *


class BlockspaceMock(BlockSpace):
    """
    Used in the command shell tests.
    """

    def __init__(self, size):
        super(BlockspaceMock, self).__init__(size)
        self._packed_blocks = {}

    @property
    def packed_blocks(self):
        """
        Get the placed blocks
        """
        return self._packed_blocks

    def add_block(self, block, location):
        """
        Add a block at a location.
        """
        self._packed_blocks[block] = location


class TestShell(TestCase):
    def setUp(self):
        self.blockspace = BlockspaceMock((20, 20, 20))
        self.executor = CommandBlock(None)
        self.executor_location = Vector(1, 2, 3)
        self.blockspace.add_block(self.executor, self.executor_location)
        self.context = ShellContext(self.blockspace, self.executor)
        self.subject_shell.context = self.context

    @property
    def subject_shell(self):
        return CommandShell(object())


class TestLocationShell(TestShell):
    # TODO: write tests for the reset of the commands.
    def setUp(self):
        super(TestLocationShell, self).setUp()
        self.blockspace.add_block(self.subject_block, Vector(2, 2, 2))

    @property
    @memoize
    def subject_block(self):
        return Block(0)

    @property
    def subject_shell(self):
        return self.subject_block.shell

    def test_location(self):
        self.assertEqual("~1 ~0 ~-1", self.subject_shell.location)

    def test_area(self):
        self.assertEqual("~1 ~0 ~-1 ~1 ~0 ~-1", self.subject_shell.area)

    def test_setblock(self):
        compiled_command = self.subject_shell.setblock(TRUE_BLOCK)()
        self.assertEqual("/setblock ~1 ~0 ~-1 redstone_block 0", compiled_command)
        compiled_command = self.subject_shell.setblock(TRUE_BLOCK, 7)()
        self.assertEqual("/setblock ~1 ~0 ~-1 redstone_block 7", compiled_command)

    def test_testforblock(self):
        compiled_command = self.subject_shell.testforblock(TRUE_BLOCK)()
        self.assertEqual("/testforblock ~1 ~0 ~-1 redstone_block 0", compiled_command)
        compiled_command = self.subject_shell.testforblock(TRUE_BLOCK, 7)()
        self.assertEqual("/testforblock ~1 ~0 ~-1 redstone_block 7", compiled_command)


class TestCommandBlockShell(TestLocationShell):
    @property
    @memoize
    def subject_block(self):
        return CommandBlock(None)

    @property
    def subject_shell(self):
        return self.subject_block.shell

    def test_has_succeeded(self):
        command_result = self.subject_shell.has_succeeded()()
        self.assertEqual("/testforblock ~1 ~0 ~-1 command_block 1 {SuccessCount: 1}", command_result)
