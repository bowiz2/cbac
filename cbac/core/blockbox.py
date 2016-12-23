"""
Holds BlockBox class
"""
from cbac.core.block import Block
from cbac.core.utils import memoize


class BlockBox(object):
    """
    A block box is a collection of blocks fit in a bound area.
    """

    def __init__(self, size, isolated=False):
        self.isolated = isolated
        self.size = size

    @property
    @memoize
    def blocks(self):
        return [[[]]]

    def __getitem__(self, item):
        return self.blocks[item]


class PlainBlockBox(BlockBox):
    """
    This is a block-box which composed of a single type of a minecraft block.
    """

    def __init__(self, size, fill_material, fill_data=0, isolated=False):
        super(PlainBlockBox, self).__init__(size, isolated)
        self.fill_material = fill_material
        self.fill_data = fill_data

    @property
    @memoize
    def blocks(self):
        return [[[Block(self.fill_material, block_data=self.fill_data) for _ in xrange(self.size[0])] for _ in
                 xrange(self.size[1])] for _ in xrange(self.size[2])]
