"""
Holds Constant class.
"""
from cbac.core.block import Block
from cbac.core.constants import block_id

from cbac.core.compound import Compound
from cbac.core.utils import memoize


# TODO: create constant factory


class HardwareConstant(Compound):
    """
    Hardware representation of a number in bits.
    When compiled, holds the binary representation of a number.
    """

    def __init__(self, number, word_size=8):
        """
        :param number: The constant value you want to store in the world, the bits of the constant represent this
        number,
        :param word_size: the number of the blocks will be completed to this size if exits.
        """
        super(HardwareConstant, self).__init__(isolated=False)
        self.word_size = word_size
        self.number = number
        self.bits = [bool(int(x)) for x in reversed(bin(number)[2:])]

    @property
    @memoize
    def blocks(self):
        """
        :return: Collection of blocks which compose this constant in the space.
        """
        to_return = []
        for bit in self.bits:
            if bit:
                material = block_id.TRUE_BLOCK
            else:
                material = block_id.FALSE_BLOCK

            to_return.append(Block(material))

        if self.word_size is not None:
            for i in xrange(self.word_size - len(self.bits)):
                to_return.append(Block(block_id.FALSE_BLOCK))
        return to_return


class ConstantFactory(object):
    """
    Creates Hardware constant objects using cache.
    """
    def __init__(self, word_size):
        """
        :param word_size: Word size of the constant.
        For example a number can be 2 but the word size is 8 resulting in 00000010
        """
        self.word_size = word_size
        self.cache = {}

def factory(number, word_size=8):
    """
    Get a constant by this number. use cache to reduce the duplication of same hardware constants.
    :param number: The value of the constant.

    """
    pass