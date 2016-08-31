from cbac.block import Block
from cbac.command_shell import RegisterShell
from cbac.compound import Compound
from cbac.constants import block_id
from cbac.utils import memoize


class Register(Compound):
    """
    An array of empty blocks which later will be used to store some data.
    """

    def __init__(self, size, default_block=block_id.FALSE_BLOCK):
        """
        :param size: Size of the memory in bits.
        """
        self.size = size
        self.default_block = default_block
        super(Register, self).__init__(isolated=True)

    @property
    @memoize
    def blocks(self):
        to_return = []
        for i in xrange(self.size):
            to_return.append(Block(self.default_block))
        return to_return

    def get_sub_memory(self, arange):
        """
        Get a sub memory of a memory.
        :param range: iterator over the blocks you want to add to the sub memory.
        :return: new memory compound which shares blocks with this memory.
        """
        sub_memory = Register(size=len(arange))
        for i, block_index in enumerate(arange):
            sub_memory.blocks[i] = self.blocks[block_index]
        return sub_memory

    @property
    @memoize
    def shell(self):
        return RegisterShell(self)
