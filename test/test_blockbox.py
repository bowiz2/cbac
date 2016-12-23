from unittest import TestCase

from cbac.core.blockbox import PlainBlockBox
from cbac.core.blockspace import BlockSpace
from cbac.core.blockspace.area import BlockBoxArea
from cbac.core.block import BlockID
from test.decorators import save_schematic
import cbac


class BlockBoxTest(TestCase):
    def test_creation(self):
        my_blockbox = PlainBlockBox((10, 3, 4), BlockID.TRUE_BLOCK)
        self.assertIsNotNone(my_blockbox[3][2][9])

    def test_area(self):
        size = (2, 3, 4)
        my_blockbox = PlainBlockBox(size, BlockID.TRUE_BLOCK)
        area = BlockBoxArea(my_blockbox)
        self.assertEqual(len(area.packed_blocks), size[0] * size[1] * size[2])

    @save_schematic
    def test_blockspace_integration(self):
        size = (2, 3, 4)
        my_blockbox = PlainBlockBox(size, BlockID.TRUE_BLOCK)
        my_blockspace = BlockSpace((20, 20, 20))
        my_blockspace.add(my_blockbox)
        my_blockspace.pack()
        return cbac.assembler.assemble(my_blockspace)

    def test_ram(self):
        ram = cbac.std_unit.ram_unit.MemoryDump([1, 2, 3])
        blockspace = BlockSpace((1, 1, 1))
        blockspace.add(ram)
        blockspace.build("./products/memory_dump.schematic")
