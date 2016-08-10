from command_shell import CompoundShell
from constants import block_id as ids
from constants import cb_action
from constants import direction
from utils import memoize


class Block(object):
    """
    Represents a block in minecraft world. to bind it to a location, use a blockspace.
    """

    def __init__(self, block_id, block_data=0, has_tile_entity=False):
        """
        :param block_id: The minecraft block id of this block, such as 0 for air and 1 for stone.
        :param block_data: Block data value.
        :param has_tile_entity: If this block has a tile entity and needs to be translated to it.
        """
        self.block_id = block_id
        self.block_data = block_data
        self.has_tile_entity = has_tile_entity

    @property
    @memoize
    def shell(self):
        return BlockShell(self)


class CommandBlock(Block):
    """
    Command Block inside minecraft.
    Contains all the command block types. Such as impulse repeat and chain.
    """

    # TODO: Use command block name as a debug tool.
    def __init__(self, command, facing=direction.UP, action=cb_action.IMPULSE, always_active=False, conditional=False,
                 custom_name=None):
        self.command = command
        self.facing = facing
        self.action = action
        self.always_active = always_active
        self.conditional = conditional
        self.custom_name = custom_name

        if self.action == cb_action.IMPULSE:  # 'impulse'
            block_id = ids.IMPULSE_COMMAND_BLOCK
        elif self.action == cb_action.REPEAT:  # 'repeat'
            block_id = ids.REPEATING_COMMAND_BLOCK
        elif self.action == cb_action.CHAIN:  # 'chain'
            block_id = ids.CHAIN_COMMAND_BLOCK
        else:
            raise TypeError("No such action {0}.".format(action))

        block_data = 1 if self.always_active else 0

        super(CommandBlock, self).__init__(block_id, block_data, has_tile_entity=True)
