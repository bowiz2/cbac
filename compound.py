from block import Block, CommandBlock
from constants import cb_action, block_id


class Compound(object):
    """Contains the blocks which are part of the compound."""
    def __init__(self, blocks, isolated=False):
        self.blocks = blocks
        self.isolated = isolated


class CBA(Compound):
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
    def __init__(self, number):
        super(Constant, self).__init__(list(), isolated=False)

        self.number = number
        self.bits = [bool(int(x)) for x in reversed(bin(number)[2:])]

        for bit in self.bits:
            if bit:
                material = block_id.TRUE_BLOCK
            else:
                material = block_id.FALSE_BLOCK

            self.blocks.append(Block(material))


class Memory(Compound):
    def __init__(self, size, isolated=False):
        """
        :param size: Size of the memory in bits.
        """
        self.size = 0
        super(Memory, self).__init__(list(), isolated)

        for i in xrange(size):
            self.blocks.append(Block(block_id.EMPTY_BLOCK))
