from unittest import TestCase

from cbac.core.blockbox import BlockBox
from cbac.core.blockspace import BlockSpace
from cbac.core.blockspace.area import BlockBoxArea
from cbac.core.constants.block_id import REDSTONE_BLOCK
from test.decorators import save_schematic
import cbac

class BlockBoxTest(TestCase):
    def test_creation(self):
        my_blockbox = BlockBox((10, 3, 4), REDSTONE_BLOCK)
        self.assertIsNotNone(my_blockbox[9][2][3])

    def test_area(self):
        size = (2, 3, 4)
        my_blockbox = BlockBox(size, REDSTONE_BLOCK)
        area = BlockBoxArea(my_blockbox)
        self.assertEqual(len(area.packed_blocks), size[0] * size[1] * size[2])

    @save_schematic
    def test_blockspace_integration(self):
        size = (2, 3, 4)
        my_blockbox = BlockBox(size, REDSTONE_BLOCK)
        my_blockspace = BlockSpace((20, 20, 20))
        my_blockspace.add(my_blockbox)
        my_blockspace.pack()
        return cbac.assembler.build(my_blockspace)
