from cbac.block import Block


class BlockBox(object):
    """
    A block box is a collection of blocks fit in a bound area.
    """
    def __init__(self, size, fill_material):
        self.size = size
        self.fill_material = fill_material
        self.blocks = [
            [[Block(self.fill_material) for _ in xrange(size[0])] for _ in xrange(size[1])] for _ in xrange(size[2])
            ]