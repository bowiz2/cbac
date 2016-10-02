from cbac.block import Block


class BlockBox(object):
    """
    A block box is a collection of blocks fit in a bound area.
    """

    def __init__(self, size, fill_material, fill_data=0, isolated=False):
        self.isolated = isolated
        self.size = size
        self.fill_material = fill_material
        self.blocks = [
            [[Block(self.fill_material, block_data=fill_data) for _ in xrange(size[2])] for _ in xrange(size[1])] for _
            in xrange(size[0])
            ]

    def __getitem__(self, item):
        return self.blocks[item]
