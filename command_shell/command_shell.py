from . import ShellContext, CommandSuspender
from constants.block_id import TRUE_BLOCK, FALSE_BLOCK
from constants.block_id import names as block_names


def command(creates_condition=None):
    """
    :param creates_condition: whenever this command creates condition.
    :return: command decorator.
    """

    def command_decorator(f):
        """
        Makes this function a suspended method. decorator
        """

        def _wrapper(self, *args, **kwargs):
            sus = CommandSuspender(self, f, *args, **kwargs)
            sus.creates_condition = creates_condition
            return sus

        return _wrapper

    return command_decorator


class CommandShell(object):
    """
    A command command_shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """

    def __init__(self, wrapped, context=(None, None)):
        """
        :param wrapped: The object which this command command_shell is wrapping.
        :param context
        """
        self.wrapped = wrapped
        # Coupling.
        if not isinstance(context, ShellContext):
            context = ShellContext(*context)
        self.context = context

    @staticmethod
    def _join_command(*items):
        # TODO: implement test.
        return " ".join([str(item) for item in items if item is not None])


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

        ds = map(str, location)

        if self.context.executor is not None:
            ds = ['~' + d for d in ds]

        return " ".join(ds)

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
        # TODO: fix this ugly as f.
        if self.context.executor is None:
            point_a, point_b = self.context.get_absolute_area(self.wrapped)
        else:
            point_a, point_b = self.context.get_relative_area(self.wrapped)

        point_a = map(str, point_a)
        point_b = map(str, point_b)
        ds = point_a + point_b
        if self.context.executor is not None:
            ds = ['~' + d for d in ds]
        return " ".join(ds)

    @command()
    def clone(self, other, mask_mode="replace", clone_mode="normal", tile_name=None):
        """
        Clone this compound to another area.
        """
        if mask_mode == "filtered":
            assert tile_name is not None

        other.shell.context = self.context
        return self._join_command("/clone", self.area, other.shell.location, mask_mode, clone_mode, tile_name)

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


class CompoundShell(LocationShell):
    """
    Provides commands for manipulating compounds inside Minecraft.
    """

    @command(True)
    def testforblocks(self, other):
        other.shell.context = self.context
        return "/testforblocks {0} {1}".format(self.area, other.shell.location)

    def __eq__(self, other):
        """
        Check if this compound has the same blocks as other thing.
        :return: CommandSuspender
        """
        return self.testforblocks(other)


# A block has only a location. so it is very reasonable to have the same command_shell as the location command_shell.
BlockShell = LocationShell
