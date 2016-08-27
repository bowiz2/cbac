from unittest import TestCase

import cbac


class TestBlock(TestCase):
    def test_command_block(self):
        cb = cbac.block.CommandBlock("/say hello", facing=cbac.block.mc_direction.SOUTH, action="chain")
        self.assertEqual(cb.command, "/say hello")
        redstone = cbac.block.Block(cbac.block.ids.REDSTONE_BLOCK)
        return None
