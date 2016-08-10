from unittest import TestCase

import block


class TestBlock(TestCase):
    def test_block(self):
        cb = block.CommandBlock("/say hello", facing=block.direction.SOUTH, action=block.cb_action.CHAIN)
        redstone = block.Block(block.ids.REDSTONE_BLOCK)
        return None
