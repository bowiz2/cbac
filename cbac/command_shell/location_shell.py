from .command_shell_base import CommandShell
from cbac.constants.block_id import names as block_names, TRUE_BLOCK, FALSE_BLOCK
from .decorator import command
from cbac.utils import format_location, format_realtive_location

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

    @command(creates_condition=True)
    def testforblock(self, block_id, data_value=None, tags=None):
        """
        Test if this location object is of the certain type.
        """
        return " ".join([str(item) for item in
                         ["/testforblock", self.location, block_names[block_id], data_value, tags]
                         if item is not None])

    @command()
    def setblock(self, block_id, data_value=None, block_handling=None, tags=None):
        """
        Sets a block to a new block id
        """
        return self._join_command("/setblock", self.location, block_names[block_id], data_value, block_handling, tags)

    def activate(self):
        return self.setblock(TRUE_BLOCK)

    def deactivate(self):
        return self.setblock(FALSE_BLOCK)

    @property
    def area(self):
        # TODO: write test.
        if self.context.executor is None:
            area = self.context.get_absolute_area(self.wrapped)
            formatted_area = [format_location(point) for point in area]
        else:
            area = self.context.get_relative_area(self.wrapped)
            formatted_area = [format_realtive_location(point) for point in area]

        return " ".join(formatted_area)

    @command()
    def clone(self, other, mask_mode="replace", clone_mode="normal", tile_name=None):
        """
        Clone this compound to another area.
        """
        if mask_mode == "filtered":
            assert tile_name is not None

        other.shell.context = self.context
        return self._join_command("/clone", self.area, other.shell.location, mask_mode, clone_mode, tile_name)

    def copy(self, other):
        """
        Copy this compound to another area. Alias for clone.
        """
        return self.clone(other)

    @command()
    def fill(self, block_id, data_value=None, block_handling=None, *options):
        """
        Fill this compound with a block.
        :param block_id: id of the block
        :param data_value: data value of the block
        :param block_handling: fill mode
        :param tags:
        """

        return self._join_command("/fill", self.area, block_names[block_id], data_value, block_handling, *options)

    def replace(self, block_id, other_block_id, block_data_value=0, other_block_data_value=0):
        return self.fill(
            other_block_id,
            other_block_data_value,
            "replace",
            block_names[block_id],
            block_data_value
        )

    def move(self, target):
        return self.clone(target, clone_mode="move")

    def __eq__(self, other):
        """
        This is used for conditionning in the condition unit.
        :param other: some block you want to test against.
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


BlockShell = LocationShell
