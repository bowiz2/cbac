from block import Block, CommandBlock
from constants.block_id import FALSE_BLOCK
from constants import cb_action, block_id
from command_shell import BlockShell


class Compound(object):
    """Contains the blocks which are part of the compound. Later can be bound to a blockspace."""
    def __init__(self, blocks, isolated=False):
        self.blocks = blocks
        self.isolated = isolated


class CBA(Compound):
    """
    Command Block Array
    """
    created_count = 0

    def __init__(self, *commands):
        self.cba_id = self.created_count
        self.created_count += 1
        self.name = "CBA_n{0}".format(self.cba_id)
        self.activator = Block(FALSE_BLOCK)

        blocks = list(self._gen_cb_chain(list(commands) + [BlockShell(self.activator).deactivate()]))

        # create activator block.

        blocks = [self.activator] + blocks

        for i, block in enumerate(blocks):
            block.custom_name = "{cba_name}[{i}]".format(cba_name=self.name, i=i)
            try:
                if block.command.creates_condition:
                    # make the next block conditional.
                    next_block = blocks[i+1]
                    next_block.conditional = True
            except IndexError:
                pass  # if there is not next block.
            except AttributeError:
                pass # in-case this was not a command block or the next block had no conditional option.

        super(CBA, self).__init__(blocks, isolated=True)

    @staticmethod
    def _gen_cb_chain(commands):
        assert len(commands) > 0

        yield CommandBlock(commands[0], facing=None, action=cb_action.IMPULSE)

        for command in commands[1:]:
            yield CommandBlock(command, facing=None, action=cb_action.CHAIN, always_active=True)

    def __str__(self):
        return self.name


class Extender(CBA):
    def __init__(self, *targets):
        super(Extender, self).__init__(*[BlockShell(target.activator).activate() for target in targets])


class IfFlow(CBA):
    def __init__(self, condition, target):
        super(IfFlow, self).__init__(condition, BlockShell(target.activator).activate())


class SwitchFlow(CBA):
    def __init__(self, cases):
        commands = list()
        for condition, target in cases.items():
            commands.append(condition)
            commands.append(BlockShell(target.activator).activate())
        super(SwitchFlow, self).__init__(commands)


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
                self.blocks.append(Block(block_id.FALSE_BLOCK))


class Memory(Compound):
    """
    An array of empty blocks which later will be used to store some data.
    """
    def __init__(self, size):
        """
        :param size: Size of the memory in bits.
        """
        self.size = 0
        super(Memory, self).__init__(list(), isolated=True)

        for i in xrange(size):
            self.blocks.append(Block(block_id.EMPTY_BLOCK))
