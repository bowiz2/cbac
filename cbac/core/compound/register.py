from cbac.core.block import Block
from cbac.core.command_shell import RegisterShell
from cbac.core.constants import block_id

from cbac.core.compound import Compound
from cbac.core.utils import memoize


class Register(Compound):
    """
    An array of empty blocks which later will be used to store some data.
    """
    # TODO: important! merge hardware constant and register.
    def __init__(self, size, default_block=block_id.FALSE_BLOCK):
        """
        :param size: Size of the memory in bits.
        """
        self.size = size
        self.default_block = default_block
        self._value = 0
        super(Register, self).__init__(isolated=False)

    @property
    @memoize
    def blocks(self):
        """
        :return: List of blocks which compose the register.
        """
        bits = bin(self._value)[2:]
        pad = self.size - len(bits)
        assert pad >= 0, "value is too big."
        bits += ('0' * pad)
        _blocks = []
        for bit in bits:
            material = block_id.TRUE_BLOCK if bit == '0' else block_id.FALSE_BLOCK
            _blocks.append(Block(material))
        return _blocks

    @property
    def ports(self):
        """
        :return: All the ports in this register.
        """
        return self.blocks

    def slice(self, arange):
        """
        Get a sub memory of a memory.
        :param arange: iterator over the blocks you want to add to the sub memory.
        :return: new memory compound which shares blocks with this memory.
        """
        sub_memory = Register(size=len(arange))
        # Set the corresponding blocks in the range to the blocks in the slice.
        for i, block_index in enumerate(arange):
            sub_memory.blocks[i] = self.blocks[block_index]
        return sub_memory

    def set_initial_value(self, value):
        """
        Set the initial value of the register
        """
        self._value = value

    @property
    @memoize
    def shell(self):
        return RegisterShell(self)
