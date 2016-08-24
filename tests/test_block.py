from unittest import TestCase

import block
import cbac


class TestBlock(TestCase):
    def test_block(self):
        cb = cbac.block.CommandBlock("/say hello", facing=cbac.block.mc_direction.SOUTH, action="chain")
        redstone = cbac.block.Block(cbac.block.ids.REDSTONE_BLOCK)
        return None
