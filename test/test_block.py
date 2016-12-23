from unittest import TestCase
import cbac
from cbac.core.block import BlockID


class TestBlock(TestCase):
    def test_command_block(self):
        cb = cbac.CommandBlock("/say hello", facing=cbac.MCDirection.SOUTH, action="chain")
        self.assertEqual(cb.command, "/say hello")
        redstone = cbac.Block(BlockID.REDSTONE_BLOCK)
        return None
