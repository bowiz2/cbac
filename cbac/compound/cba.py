from cbac.block import Block, CommandBlock
from cbac.command_shell import CBAShell
from cbac.compound import Compound
from cbac.constants.block_id import FALSE_BLOCK
from cbac.utils import memoize


class CBA(Compound):
    """
    Command Block Array
    """
    created_count = 0

    def __init__(self, *commands):
        self.cba_id = self.created_count
        self.created_count += 1

        self.commands = commands

        # commands
        self.user_command_blocks = list(self._gen_cb_chain(commands))

        # An empty block which when activated. will fire up this cba.
        self.activator = Block(FALSE_BLOCK)

        # This block responsible for deactivating the activator block.
        self.cb_re_setter = CommandBlock(self.activator.shell.deactivate(), None, "chain", True)
        # This command block is reserved for callback use.
        self.cb_callback_reserved = CommandBlock("", None, "chain", True)

        blocks = self.system_prefix_blocks + self.user_command_blocks + self.system_postfix_blocks

        blocks = self.set_block_names(blocks)

        blocks = self.bind_conditions(blocks)

        super(CBA, self).__init__(blocks, isolated=True)

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

    @staticmethod
    def _gen_cb_chain(commands):
        """
        Wrappes commands in command blocks, and according to their position decide If they need to be impulse command
            blocks or chain command blocks.
        :param commands: a list of commands.
        :return: CommandBlock generator.
        """
        assert len(commands) > 0

        yield CommandBlock(commands[0], facing=None, action="impulse")

        for command in commands[1:]:
            yield CommandBlock(command, facing=None, action="chain", always_active=True)

    @property
    @memoize
    def shell(self):
        return CBAShell(self)

    @property
    def system_prefix_blocks(self):
        return [self.activator]

    @property
    def system_postfix_blocks(self):
        return [self.cb_callback_reserved, self.cb_re_setter]

    @property
    def name(self):
        return "CBA_n{0}".format(self.cba_id)

    def __add__(self, other):
        """
        Create a new cba out of this cba's commands and the other cba's commands.
        :param other: Another cba.
        :return: A new cba.
        """
        return CBA(*[self.commands + other.commands])

    def __str__(self):
        return self.name
