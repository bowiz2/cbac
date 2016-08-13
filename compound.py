from block import Block, CommandBlock
from command_shell import CompoundShell, CBAShell
from command_shell.location_shell import BlockShell
from command_shell.memory_shell import MemoryShell
from constants import cb_action, block_id
from constants.block_id import FALSE_BLOCK
from utils import memoize


class Compound(object):
    """Contains the blocks which are part of the compound. Later can be bound to a blockspace."""

    def __init__(self, blocks, isolated=False):
        self.blocks = blocks
        self.isolated = isolated

    @property
    @memoize
    def shell(self):
        return CompoundShell(self)


class CBA(Compound):
    """
    Command Block Array
    """
    created_count = 0

    def __init__(self, *commands):
        self.cba_id = self.created_count
        self.created_count += 1
        self.name = "CBA_n{0}".format(self.cba_id)

        # commands
        self.user_command_blocks = list(self._gen_cb_chain(commands))

        # An empty block which when activated. will fire up this cba.
        self.activator = Block(FALSE_BLOCK)
        self.system_prefix_blocks = [self.activator]

        # This block responsible for deactivating the activator block.
        self.cb_re_setter = CommandBlock(self.activator.shell.deactivate(), None, cb_action.CHAIN, True)
        # This command block is reserved for callback use.
        self.cb_callback_reserved = CommandBlock("", None, cb_action.CHAIN, True)

        self.system_postfix_blocks = [self.cb_callback_reserved, self.cb_re_setter]

        blocks = self.system_prefix_blocks + self.user_command_blocks + self.system_postfix_blocks

        for i, block in enumerate(blocks):
            # create custom names for blocks.
            block.custom_name = "{cba_name}[{i}]".format(cba_name=self.name, i=i)
            try:
                action = "<{0}>".format(block.command.command_function.__name__)
                block.custom_name += action
            except AttributeError:
                pass
            # Parse conditionaning.
            try:
                if block.command.creates_condition:
                    # make the next block conditional.
                    next_block = blocks[i + 1]
                    next_block.conditional = True
            except IndexError:
                pass  # if there is not next block.
            except AttributeError:
                pass  # in-case this was not a command block or the next block had no conditional option.

        super(CBA, self).__init__(blocks, isolated=True)

    @staticmethod
    def _gen_cb_chain(commands):
        assert len(commands) > 0

        yield CommandBlock(commands[0], facing=None, action=cb_action.IMPULSE)

        for command in commands[1:]:
            yield CommandBlock(command, facing=None, action=cb_action.CHAIN, always_active=True)

    @property
    @memoize
    def shell(self):
        return CBAShell(self)

    def __str__(self):
        return self.name


class IfFlow(CBA):
    """
    Target is activated when the condition command is sucsessfull.
    """

    def __init__(self, condition, target):
        super(IfFlow, self).__init__(condition, target.activator.shell.activate())


class SwitchFlow(CBA):
    """
    Switches to a case given an item.
    """

    def __init__(self, item, cases):
        commands = list()
        self.comparables = list()
        for value, target in cases.items():
            commands.append(item.shell == value)
            try:
                commands.append(target.activator.shell.activate())
            except AttributeError:
                commands.append(target)
            self.comparables.append(value)
        super(SwitchFlow, self).__init__(*commands)


class Extender(CBA):
    """
    When you activate this CBA, it will activate all the targets.
    """

    def __init__(self, *targets):
        super(Extender, self).__init__(*[BlockShell(target.activator).activate() for target in targets])


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


class Memory(Compound):
    """
    An array of empty blocks which later will be used to store some data.
    """

    def __init__(self, size):
        """
        :param size: Size of the memory in bits.
        """
        self.size = size
        super(Memory, self).__init__(list(), isolated=True)

        for i in xrange(size):
            self.blocks.append(Block(block_id.FALSE_BLOCK))

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
