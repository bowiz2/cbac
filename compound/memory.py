from block import Block
from command_shell import MemoryShell
from compound.compound import Compound
from constants import block_id
from utils import memoize


class Memory(Compound):
    """
    An array of empty blocks which later will be used to store some data.
    """

    def __init__(self, size, default_block=block_id.FALSE_BLOCK):
        """
        :param size: Size of the memory in bits.
        """
        self.size = size
        self.default_block = default_block
        super(Memory, self).__init__(list(), isolated=True)

        for i in xrange(size):
            self.blocks.append(Block(self.default_block))

    def get_sub_memory(self, arange):
        """
        Get a sub memory of a memory.
        :param range: iterator over the blocks you want to add to the sub memory.
        :return: new memory compound which shares blocks with this memory.
        """
        sub_memory = Memory(size=len(arange))
        for i, block_index in enumerate(arange):
            sub_memory.blocks[i] = self.blocks[block_index]
        return sub_memory

    @property
    @memoize
    def shell(self):
        return MemoryShell(self)