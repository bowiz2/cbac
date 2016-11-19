"""
Holds Minecraft block class.
"""
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
        :param has_tile_entity: If this block has a tile mcentity and needs to be translated to it.
        """
        self._block_id = block_id
        self._block_data = block_data
        self.has_tile_entity = has_tile_entity

    @property
    def block_id(self):
        """
        The minecraft block type id of this block
        :return: number
        """
        return self._block_id

    @property
    def block_data(self):
        """
        :return: Minecraft block data.
        """
        return self._block_data

    @property
    @memoize
    def shell(self):
        """
        :return: Minecraft command interface.
        """

        from command_shell.location_shell import BlockShell
        return BlockShell(self)

    def __str__(self):
        return "{0} Block".format(ids.names[self.block_id])


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
        super(CommandBlock, self).__init__(self.block_id, 0, has_tile_entity=True)

    @property
    def block_id(self):
        """
        Minecraft block id of the command blocks
        :note: depends on the action of the block.
        """
        if self.action == "impulse":
            return ids.IMPULSE_COMMAND_BLOCK
        elif self.action == "repeat":  # 'repeat'
            return ids.REPEATING_COMMAND_BLOCK
        elif self.action == "chain":  # 'chain'
            return ids.CHAIN_COMMAND_BLOCK
        else:
            raise TypeError("No such action {0}.".format(self.action))

    @property
    def block_data(self):
        """
        Minecraft block data
        :note: depends on hte always_active property.
        """
        if self.always_active:
            return 1
        else:
            return 0

    @property
    def data_value(self):
        """
        :return: Data value of the block if it were placed in the world.
        """
        if self.facing is None:
            return 0

        # The data value depends on the direction the command block is facing.
        face_index = [DOWN, UP, NORTH, SOUTH, WEST, EAST].index(self.facing)

        conditional = self.conditional

        if hasattr(self.command, "is_conditional"):
            conditional = conditional or self.command.is_conditional

        # This is a weir data value computation required by minecraft. not this is bitwise calculation.
        conditional_num = 0x8 if conditional else 0
        data_value = face_index | conditional_num

        return data_value

    @property
    @memoize
    def shell(self):
        """
        :return: Minecraft command interface.
        """
        from command_shell import CommandBlockShell
        return CommandBlockShell(self)
