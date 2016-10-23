from unittest import TestCase

from cbac.core.block import Block, CommandBlock
from cbac.core.blockspace import BlockSpace
from cbac.core.command_shell import ShellContext, CommandShell
from cbac.core.constants.block_id import *
from cbac.core.command_shell.player_shell import PlayerShell
from cbac.core.utils import Vector, memoize
from cbac.core.mcentity import Player

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


class TestPlayerShell(TestShell):
    @property
    def subject_shell(self):
        return Player("test_player").shell

    def test_exists(self):
        self.assertEquals("/testfor @a[name=test_player]", self.subject_shell.test_exists().compile())

    def test_coordinates(self):
        self.assertEquals("/testfor @a[x=1,y=2,z=3,name=test_player]",
                          self.subject_shell.test_coordinate((1, 2, 3)).compile())

    def test_roatation(self):
        self.assertEquals("/testfor @a[name=test_player,rx=2,rxm=1]",
                          self.subject_shell.test_rotation_vertical(1,2).compile())
        self.assertEquals("/testfor @a[name=test_player,ry=2,rym=1]",
                          self.subject_shell.test_rotation_horizontal(1, 2).compile())
