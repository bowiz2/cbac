from block import Block
from compound.compound import Compound
from constants import block_id


class Constant(Compound):
    """
    When compiled, holds the binary representation of a number.
    """

    def __init__(self, number, buffer_size=8):
        """
        :param number: The constat value you want to store in the world, the bits of the consstant represent this number,
        :param buffer_size: the number of the blocks will be completed to this size if exits.
        """
        super(Constant, self).__init__(list(), isolated=False)

        self.number = number
        self.bits = [bool(int(x)) for x in reversed(bin(number)[2:])]

        for bit in self.bits:
            if bit:
                material = block_id.TRUE_BLOCK
            else:
                material = block_id.FALSE_BLOCK

            self.blocks.append(Block(material))

        if buffer_size is not None:
            for i in xrange(buffer_size - len(self.bits)):
                self.blocks.append(Block(block_id.FALSE_BLOCK))