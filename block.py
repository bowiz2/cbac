from constants import block_id as ids
from constants import cb_action
from constants import direction


class Block(object):
    """
    Represents a block in minecraft world. to bind it to a location, use a blockspace.
    """
    def __init__(self, block_id, block_data=0, tags=None):
        self.block_id = block_id
        self.block_data = block_data
        if not tags:
            tags = {}
        self.tags = tags


class CommandBlock(Block):
    """
    Command Block inside minecraft.
    Contains all the command block types. Such as impulse repeat and chain.
    """
    def __init__(self, command, facing=direction.UP, action=cb_action.IMPULSE, always_active=False, conditional=False):
        self.command = command
        self.facing = facing
        self.action = action
        self.always_active = always_active
        self.conditional = conditional

        if self.action == cb_action.IMPULSE:  # 'impulse'
            block_id = ids.IMPULSE_COMMAND_BLOCK
        elif self.action == cb_action.REPEAT:  # 'repeat'
            block_id = ids.REPEATING_COMMAND_BLOCK
        elif self.action == cb_action.CHAIN:  # 'chain'
            block_id = ids.CHAIN_COMMAND_BLOCK
        else:
            raise TypeError("No such action {0}.".format(action))

        block_data = 1 if self.always_active else 0

        super(CommandBlock, self).__init__(block_id, block_data)
