from command_shell import CommandBlockShell
from command_shell.location_shell import BlockShell
from constants import block_id as ids
from constants import mc_direction
from constants.mc_direction import DOWN, UP, NORTH, SOUTH, WEST, EAST
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
        self._belongs_to_blockspace = False  # used for testign and debugging. TODO: consider removing

    @property
    @memoize
    def shell(self):
        return BlockShell(self)


class CommandBlock(Block):
    """
    Command Block inside minecraft.
    Contains all the command block types. Such as impulse repeat and chain.
    """

    def __init__(self, command, facing=mc_direction.UP, action="impulse", always_active=False, conditional=False,
                 custom_name=None):
        """
        :param command: The command which will be executed when this command block is activated in the "real" world.
        :param facing: The direction which the command block is facing.
        :param action: The Type of the command block. can be impulse, repeat and chain.
        :param always_active: If the command block does not need redstone current to function.
        :param conditional: If the command block is conditional.
        :param custom_name: Special name of the command block. Useful for debugging.
        """
        self.command = command
        self.facing = facing
        self.action = action
        self.always_active = always_active
        self.conditional = conditional
        self.custom_name = custom_name

        if self.action == "impulse":
            block_id = ids.IMPULSE_COMMAND_BLOCK
        elif self.action == "repeat":  # 'repeat'
            block_id = ids.REPEATING_COMMAND_BLOCK
        elif self.action == "chain":  # 'chain'
            block_id = ids.CHAIN_COMMAND_BLOCK
        else:
            raise TypeError("No such action {0}.".format(action))

        block_data = 1 if self.always_active else 0

        super(CommandBlock, self).__init__(block_id, block_data, has_tile_entity=True)

    @property
    def data_value(self):
        """
        :return: Data value of the block if it were placed in the world.
        """
        if self.facing is None:
            return 0
        faceindex = [DOWN, UP, NORTH, SOUTH, WEST, EAST].index(self.facing)

        # TODO: refactor
        try:
            conditional = self.conditional or self.command.is_conditional
        except AttributeError:
            conditional = self.conditional

        conditional_num = 0x8 if conditional else 0
        data_value = faceindex | conditional_num
        return data_value

    @property
    @memoize
    def shell(self):
        return CommandBlockShell(self)
