from block import Block, CommandBlock
from constants import cb_action, block_id


class Compound(object):
    """Contains the blocks which are part of the compound. Later can be bound to a blockspace."""
    def __init__(self, blocks, isolated=False):
        self.blocks = blocks
        self.isolated = isolated


class CBA(Compound):
    """
    Command Block Array
    """
    def __init__(self, *commands):
        blocks = list(self._gen_cb_chain(commands))
        super(CBA, self).__init__(blocks, isolated=True)

    @staticmethod
    def _gen_cb_chain(commands):
        assert len(commands) > 0

        yield CommandBlock(commands[0], facing=None, action=cb_action.IMPULSE)

        for command in commands[1:]:
            yield CommandBlock(command, facing=None, action=cb_action.CHAIN, always_active=True)


class Constant(Compound):
    """
    When compiled, holds the binary representation of a number.
    """
    def __init__(self, number, buffer_size=None):
        """
        :param number: The constat value you want to store in the world
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
                self.blocks.append(Block(block_id.EMPTY_BLOCK))

class Memory(Compound):
    """
    An array of empty blocks which later will be used to store some data.
    """
    def __init__(self, size, isolated=False):
        """
        :param size: Size of the memory in bits.
        """
        self.size = 0
        super(Memory, self).__init__(list(), isolated)

        for i in xrange(size):
            self.blocks.append(Block(block_id.EMPTY_BLOCK))
