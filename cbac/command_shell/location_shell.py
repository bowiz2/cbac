"""
Holds Location shell, and Block shell, which are the same thing.
"""
from cbac.constants.block_id import names as block_names, TRUE_BLOCK, FALSE_BLOCK
from cbac.utils import format_location, format_realtive_location
from cbac.constants.mc_direction import vectors as direction_vectors
from cbac.constants.mc_direction import EAST
from .command_shell_base import CommandShell
from .decorator import command


class LocationShell(CommandShell):
    """
    Provides commands for manipulating objects inside Minecraft which have location.
    """

    @property
    def location(self):
        """
        Construct a location of this command_shell for a context. The location is ready to use in commands.
        """
        if self.context.executor is None:
            # If there is not executor there is no location to be related to.
            location = self.context.get_absolute_location(self.wrapped)
        else:
            location = self.context.get_relative_location(self.wrapped)

        if self.context.executor is not None:
            return format_realtive_location(location)

        return format_location(location)

    @property
    def area(self):
        """
        Get the area of the wrapped object inside the blockspace.
        :return: str
        """
        # TODO: write test.
        if self.context.executor is None:
            area = self.context.get_absolute_area(self.wrapped)
            formatted_area = [format_location(point) for point in area]
        else:
            area = self.context.get_relative_area(self.wrapped)
            formatted_area = [format_realtive_location(point) for point in area]

        return " ".join(formatted_area)

    @command(creates_condition=True)
    def testforblock(self, block_id, data_value=0, tags=None):
        """
        Check if a block at this location is of a certain signature.
        """
        return self._join_command("/testforblock", self.location, block_names[block_id], data_value, tags)

    @command()
    def setblock(self, block_id, data_value=0, block_handling=None, tags=None):
        """
        Sets a block to a new block id with some more advanced options.
        """
        return self._join_command("/setblock", self.location, block_names[block_id], data_value, block_handling, tags)

    @command()
    def clone(self, other, mask_mode="replace", clone_mode="normal", tile_name=None):
        """
        Clones blocks from this region to another.
        :param other: Specifies the lower northwest corner (i.e., the smallest coordinates of each axis)
        of the destination region. May use tilde notation to specify a distance relative to the command's execution.
        :param mask_mode: Specifies whether to filter the blocks being cloned. Can be filtered, masked or replace.
        :param clone_mode: Specifies how to treat the source region. Can be force, move and normal.
        :param tile_name: Specifies the block id to copy when maskMode is set to filtered. Required by filtered mode.
        :return: Clone command suspender.
        """
        assert mask_mode in ["filtered", "masked", "replace"]
        assert clone_mode in ["force", "move", "normal"]

        if mask_mode == "filtered":
            assert tile_name is not None

        other.shell.context = self.context
        return self._join_command("/clone", self.area, other.shell.location, mask_mode, clone_mode, tile_name)

    @command()
    def fill(self, block_id, data_value=None, block_handling=None, *options):
        """
        Fill this area with a block of a specific id.
        :param block_id: id of the block
        :param data_value: data value of the block
        :param block_handling: fill mode
        :param options:
        """

        return self._join_command("/fill", self.area, block_names[block_id], data_value, block_handling, *options)

    @command()
    def load_for_point_of_reference(self):
        """
        clone  from the point of reference  area to this point.
        "Point of reference" is the location (0,0,0) in this minecraft world.
        :return: CommandSuspender
        :note: Sees use in the RAM standard unit.
        """
        # TODO: fix this mess.
        return self._join_command(
            "/clone",
            format_location((0, 0, 0)),
            format_location(direction_vectors[EAST] * len(self.wrapped.blocks)),
            self.location)

    @command()
    def write_to_point_of_reference(self):
        """
        clone this area to the point of reference which is the location (0,0,0) in this minecraft world
        :return: CommandSuspender
        :note: Sees use in the RAM standard unit.
        """
        return self._join_command(
            "/clone",
            self.area,
            format_location((0, 0, 0)), )

    def copy(self, other):
        """
        Alias for the clone command.
        :param other: The location you want to copy this area to.
        :return: clone command.
        """
        return self.clone(other)

    def activate(self):
        """
        :return: Setblock command which places a true block.
        """
        return self.setblock(TRUE_BLOCK)

    def deactivate(self):
        """
        :return: Setblock command which places a false block.
        """
        return self.setblock(FALSE_BLOCK)

    def replace(self, block_id, other_block_id, block_data_value=0, other_block_data_value=0):
        """
        Replaces all the blocks in this area with a given id in a specific area with another block id.
        :param block_id: The block id you want to replace
        :param other_block_id: The block id you want to replace the first block id with.
        :param block_data_value: The data value of the block you want to replace.
        :param other_block_data_value: The data value you want to replace the block to.
        :return: Fill command. note that this fill command is with the 'replace' mode.
        """
        return self.fill(
            other_block_id,
            other_block_data_value,
            "replace",
            block_names[block_id],
            block_data_value
        )

    def move(self, target):
        """
        Moves this area to another location, not leaving any blocks behind.
        :param target: The position you want to copy this area to.
        :return: clone command.
        """
        return self.clone(target, clone_mode="move")

    def __eq__(self, other):
        """
        This is used for conditionning in the condition unit.
        :param other: some block you want to test against.
        :returns: A testforblock command.
        """
        # Work only with boolean values.
        if other is True:
            other = TRUE_BLOCK
        elif other is False:
            other = FALSE_BLOCK

        try:
            return self.testforblock(other.block_id)
        except AttributeError:
            return self.testforblock(other)

# A block has only a location. so it is very reasonable to have the same command_shell as the location command_shell.
BlockShell = LocationShell
