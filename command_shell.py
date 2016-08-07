from constants.block_id import TRUE_BLOCK, FALSE_BLOCK
from constants.block_id import names as block_names
# Selectors
NEAREST_PLAYER = '@p'
RANDOM_PLAYER = '@r'
ALL_PLAYERS = '@a'
ALL_ENTITIES = '@e'


class CommandSuspender(object):
    def __init__(self, command_shell, command_function, *args, **kwargs):
        # The command shell which created the command.
        self.command_shell = command_shell
        # The actual command function which was suspended.
        self.command_function = command_function
        # The args which will be used when the command function will be resumed
        self.args = args
        self.kwargs = kwargs
        # If the command creates conditioning for other commands. testforblock for example, creates conditioning.
        self.creates_condition = False

    def __call__(self):
        return self.command_function(self.command_shell, *self.args, **self.kwargs)


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
    A command shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """
    def __init__(self, wrapped, blockspace=None, executor=None):
        """
        :param wrapped: The object which this command shell is wrapping.
        :param blockspace: The blockspace the wrapped object is located at. will be bound later by the assembler.
        :param executor: the place from where the commands will be executed. will be bound later by the assembler.
        """
        self. wrapped = wrapped
        self.blockspace = blockspace
        self.executor = executor

    @command
    def raw(self, cmd):
        return cmd


class LocationShell(CommandShell):
    """
    Provides commands for manipulating objects inside Minecraft which have location.
    """
    @property
    def location(self):
        location = self._location if self.executor is None else self.get_relative_location(self.executor)
        ds = map(str, location)
        if self.executor is not None:
            ds = ['~' + d for d in ds]
        return " ".join(ds)

    @property
    def _location(self):
        return self.blockspace.get_location_of(self.wrapped)

    def get_relative_location(self, thing):
        return self._location - self.blockspace.get_location_of(thing)

    @command(True)
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
        Clone this compound to another area.
        """
        return " ".join([str(item) for item in
                         ["/setblock", self.location, block_names[block_id], data_value, block_handling, tags]
                         if item is not None])

    def activate(self):
        return self.setblock(TRUE_BLOCK)

    def deactivate(self):
        return self.setblock(FALSE_BLOCK)

    def __eq__(self, other):
        """
        This is used for conditionning in the condition unit.
        :param other: some block you want to test against.
        """
        try:
            return self.testforblock(other.block_id)
        except AttributeError:
            return self.testforblock(other)


class CompoundShell(LocationShell):
    """
    Provides commands for manipulating compounds inside Minecraft.
    """
    @property
    def area(self):
        # TODO: fix this ugly as f.
        point_a, point_b = self._area if self.executor is None else self.get_relative_area(self.executor)
        point_a = map(str, point_a)
        point_b = map(str, point_b)
        ds = point_a + point_b
        if self.executor is not None:
            ds = ['~' + d for d in ds]
        return " ".join(ds)

    @property
    def _area(self):
        # TODO: implement caching.
        return self.blockspace.get_area_of(self.wrapped)

    def get_relative_area(self, thing):
        point_a, point_b = self._area
        return (point_a - self.blockspace.get_location_of(thing)), (point_b - self.blockspace.get_location_of(thing))

    @command()
    def clone(self, other):
        """
        Clone this compound to another area.
        """
        try:
            location = other.location
        except AttributeError:
            # TODO: clone to area.
            location = other

        return "/clone {0} {1}".format(self.area, location)

    @command()
    def fill(self, block_id, data_value=None, block_handling=None, tags=None):
        """
        Clone this compound to another area.
        """

        return " ".join([str(item) for item in
                         ["/fill", self.area, block_names[block_id], data_value, block_handling, tags]
                         if item is not None])

    @command(True)
    def testforblocks(self, other):
        other = other.shell
        # TODO: remove hack.
        other.blockspace = self.blockspace
        other.executor = self.executor
        location = other.location

        return "/testforblocks {0} {1}".format(self.area, location)

    def __eq__(self, other):
        """
        Check if this compound has the same blocks as other thing.
        :return: CommandSuspender
        """
        return self.testforblocks(other)


# A block has only a location. so it is very reasonable to have the same shell as the location shell.
BlockShell = LocationShell
