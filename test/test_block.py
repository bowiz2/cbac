from unittest import TestCase
import cbac
import core.block


class TestBlock(TestCase):
    def test_command_block(self):
        cb = cbac.CommandBlock("/say hello", facing=cbac.MCDirection.SOUTH, action="chain")
        self.assertEqual(cb.command, "/say hello")
        redstone = cbac.Block(core.block.BlockID.REDSTONE_BLOCK)
        return None
