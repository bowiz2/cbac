"""
Holds Minecraft block class.
"""
from cbac.core.mc_direction import MCDirection
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
        return "{0} Block".format(BlockID.names[self.block_id])


class CommandBlock(Block):
    """
    Command Block inside minecraft.
    Contains all the command block types. Such as impulse repeat and chain.
    """

    def __init__(self, command, facing=MCDirection.UP, action="impulse", always_active=False, conditional=False,
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
            return BlockID.IMPULSE_COMMAND_BLOCK
        elif self.action == "repeat":  # 'repeat'
            return BlockID.REPEATING_COMMAND_BLOCK
        elif self.action == "chain":  # 'chain'
            return BlockID.CHAIN_COMMAND_BLOCK
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
        face_index = [MCDirection.DOWN, MCDirection.UP, MCDirection.NORTH, MCDirection.SOUTH, MCDirection.WEST,
                      MCDirection.EAST].index(self.facing)

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


class BlockID(object):
    """
    Block-ID Constants and util methods and variables.
    """
    EMPTY_BLOCK = 0
    AIR_BLOCK = EMPTY_BLOCK
    GLASS_BLOCK = 20
    SNOW_BLOCK = 80
    REDSTONE_BLOCK = 152
    EMERALD_BLOCK = 133
    # A block which represents the "true" value.
    TRUE_BLOCK = REDSTONE_BLOCK
    # A block which represents the "false" value.
    FALSE_BLOCK = SNOW_BLOCK

    # Command block materials.
    IMPULSE_COMMAND_BLOCK = 137
    REPEATING_COMMAND_BLOCK = 210
    CHAIN_COMMAND_BLOCK = 211

    # Blocks which do not further redstone signal.
    ISOLATORS = [EMPTY_BLOCK, GLASS_BLOCK]

    names = {
        GLASS_BLOCK: 'glass',
        EMPTY_BLOCK: 'air',
        SNOW_BLOCK: 'snow',
        REDSTONE_BLOCK: 'redstone_block',
        IMPULSE_COMMAND_BLOCK: 'command_block',
        REPEATING_COMMAND_BLOCK: 'repeating_command_block',
        CHAIN_COMMAND_BLOCK: 'chain_command_block',
        EMERALD_BLOCK: 'emerald_block'
    }
