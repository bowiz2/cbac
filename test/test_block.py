from unittest import TestCase
import cbac


class TestBlock(TestCase):
    def test_command_block(self):
        cb = cbac.CommandBlock("/say hello", facing=cbac.mc_direction.SOUTH, action="chain")
        self.assertEqual(cb.command, "/say hello")
        redstone = cbac.Block(cbac.block_id.REDSTONE_BLOCK)
        return None
