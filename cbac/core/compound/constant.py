from cbac.core.block import Block
from cbac.core.constants import block_id

from cbac.core.compound import Compound
from cbac.core.utils import memoize


# TODO: create constant factory


class Constant(Compound):
    """
    When compiled, holds the binary representation of a number.
    """

    def __init__(self, number, buffer_size=8):
        """
        :param number: The constat value you want to store in the world, the bits of the consstant represent this number,
        :param buffer_size: the number of the blocks will be completed to this size if exits.
        """
        super(Constant, self).__init__(isolated=False)
        self.buffer_size = buffer_size
        self.number = number
        self.bits = [bool(int(x)) for x in reversed(bin(number)[2:])]

    @property
    @memoize
    def blocks(self):
        to_return = []
        for bit in self.bits:
            if bit:
                material = block_id.TRUE_BLOCK
            else:
                material = block_id.FALSE_BLOCK

            to_return.append(Block(material))

        if self.buffer_size is not None:
            for i in xrange(self.buffer_size - len(self.bits)):
                to_return.append(Block(block_id.FALSE_BLOCK))
        return to_return
