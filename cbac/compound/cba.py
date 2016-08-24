import block
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
        self.name = "CBA_n{0}".format(self.cba_id)

        # commands
        self.user_command_blocks = list(self._gen_cb_chain(commands))

        # An empty block which when activated. will fire up this cba.
        self.activator = Block(FALSE_BLOCK)
        self.system_prefix_blocks = [self.activator]

        # This block responsible for deactivating the activator block.
        self.cb_re_setter = CommandBlock(self.activator.shell.deactivate(), None, "chain", True)
        # This command block is reserved for callback use.
        self.cb_callback_reserved = CommandBlock("", None, "chain", True)

        self.system_postfix_blocks = [self.cb_callback_reserved, self.cb_re_setter]

        blocks = self.system_prefix_blocks + self.user_command_blocks + self.system_postfix_blocks

        for i, block in enumerate(blocks):
            # create custom names for blocks.
            # TODO: make more readable.

            # Deprecated.
            block.custom_name = "{cba_name}[{i}]".format(cba_name=self.name, i=i)
            try:
                action = "<{0}>".format(block.command.command_function.__name__)
                block.custom_name += action
            except AttributeError:
                pass
            # end of deprecated.

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

        yield CommandBlock(commands[0], facing=None, action="impulse")

        for command in commands[1:]:
            yield CommandBlock(command, facing=None, action="chain", always_active=True)

    @property
    @memoize
    def shell(self):
        return CBAShell(self)

    def __str__(self):
        return self.name