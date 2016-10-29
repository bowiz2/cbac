"""
Command Block Array holder
"""
from cbac.core.block import Block, CommandBlock
from cbac.core.command_shell import CBAShell
from cbac.core.constants.block_id import FALSE_BLOCK

from cbac.core.compound import Compound
from cbac.core.utils import memoize


class CBA(Compound):
    """
    Command Block Array
    This is a very important class! this is the base for all the logic inside the framework.
    """
    # Track the number of cbas created. used for doc. The number is in list to become immutable.
    created_count = [0]

    def __init__(self, *commands):
        self.cba_id = self.created_count[0]
        self.created_count[0] += 1

        self.commands = commands

        # An empty block which when activated. will fire up this cba.
        self.activator = Block(FALSE_BLOCK)

        self.cb_reserved = CommandBlock("/say reserved", None, "chain", True)
        # This block responsible for deactivating the activator block. if the cba is not repeated.
        self.cb_re_setter = CommandBlock(self.activator.shell.deactivate(), None, "chain", True)

        super(CBA, self).__init__(isolated=True)

    def set_block_names(self, blocks):
        """
        Iterate over blocks and given them names according to their position in the array.
        :param blocks: blocks which you want ot name.
        :return: blocks
        """
        for i, block in enumerate(blocks):
            if hasattr(block, "custom_name"):
                block.custom_name = "{cba_name}[{i}]".format(cba_name=self.name, i=i)
        return blocks

    def set_repeat(self):
        """
        Turns this cba into a repeater. Meaning the first block of this compound is a repeat command block which is
        going to execute its command and all subsequent command each game tick as long as this compound is activated.
        :return:
        """
        assert len(self.blocks) > 2 and isinstance(self.blocks[0], CommandBlock),\
            "There must be at least 1 command block in this CBA."
        # Disable the re-setter
        self.cb_re_setter = None
        # Set the first command block to the repeat block.
        self.blocks[1].action = "repeat"

    @staticmethod
    def bind_conditions(blocks):
        """
        for each condition creating block, set the next block as conditional.
        :param blocks: list of blocks.
        :return: blocks.
        """
        for i, block in enumerate(blocks):
            try:
                if block.command.creates_condition:
                    # make the next block conditional.
                    next_block = blocks[i + 1]
                    next_block.conditional = True
            except IndexError:
                pass  # if there is not next block.
            except AttributeError:
                pass  # in-case this was not a command block or the next block had no conditional option.
        return blocks

    @property
    def user_command_blocks(self):
        """
        :return: List of command blocks which wrap user commands.
        """
        return list(self._gen_cb_chain(self.commands))

    @staticmethod
    def _gen_cb_chain(commands):
        """
        Wrappes commands in command blocks, and according to their position decide If they need to be impulse command
            blocks or chain command blocks.
        :param commands: a list of commands.
        :return: CommandBlock generator.
        """
        assert len(commands) > 0
        # The first block must be an impulse block.
        yield CommandBlock(commands[0], facing=None, action="impulse")

        # And each one after that must be chain
        for command in commands[1:]:
            yield CommandBlock(command, facing=None, action="chain", always_active=True)

    @property
    def blocks(self):
        """
        :return: Command block arrays.
        """

        to_return = self.system_prefix_blocks + self.user_command_blocks + self.system_postfix_blocks
        to_return = self.set_block_names(to_return)
        to_return = self.bind_conditions(to_return)

        return to_return

    @property
    @memoize
    def shell(self):
        """
        :return: CBAShell
        """
        return CBAShell(self)

    @property
    def system_prefix_blocks(self):
        """
        :return: Blocks which are placed before the user commands.
        """
        return [self.activator]

    @property
    def system_postfix_blocks(self):
        """
        :return: Blocks which follow the user command blocks.
        """
        return filter(lambda item: item is not None, [self.cb_re_setter])

    @property
    def name(self):
        """
        :return: The name of the cba.
        """
        return "CBA_n{0}".format(self.cba_id)

    @property
    def is_active_bit(self):
        """
        This bit indicates if the cba is currently active.
        :return: Block
        """
        return self.activator

    @property
    def is_repeat(self):
        """
        :return: True if the type of this cba is a repeater.
        """
        # The length of this cba is 1 or less it cannot be repeated.
        if len(self.blocks) <= 1:
            return False

        return isinstance(self.blocks[1], CommandBlock) and self.blocks[1].action is "repeat"

    def __add__(self, other):
        """
        Create a new cba out of this cba's commands and the other cba's commands.
        :param other: Another cba.
        :return: A new cba.
        """
        return CBA(*(self.commands + other.commands))

    def __str__(self):
        return self.name
