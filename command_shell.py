from constants.block_id import TRUE_BLOCK, FALSE_BLOCK
from constants.block_id import names as block_names


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

    def __init__(self, wrapped, context=(None, None)):
        """
        :param wrapped: The object which this command shell is wrapping.
        :param context
        """
        self.wrapped = wrapped
        # Coupling.
        if not isinstance(context, ShellContext):
            context = ShellContext(*context)
        self.context = context

    @command()
    def raw(self, cmd):
        return cmd


class ShellContext(object):
    """
    A context is the state from which the commands in the command shell are compiled.
    """

    def __init__(self, blockspace, executor):
        """
        :param blockspace: The blockspace the wrapped object is located at. will be bound later by the assembler.
        :param executor: the place from where the commands will be executed. will be bound later by the assembler.
        """
        self.blockspace = blockspace
        self.executor = executor

    def get_absolute_location(self, thing):
        """
        Get the absolute location of an object. In the context of the blockspace.
        """
        return self.blockspace.get_location_of(thing)

    def get_relative_location(self, thing):
        """
        Get hte location of an object, in relation to the executor in the context of the blockspace.
        """
        return self.get_absolute_location(thing) - self.blockspace.get_location_of(self.executor)

    def get_absolute_area(self, thing):
        # TODO: implement caching.
        return self.blockspace.get_area_of(thing)

    def get_relative_area(self, thing):
        thing_area = self.get_absolute_area(thing)
        executor_area = self.get_absolute_area(self.executor)

        return tuple([thing_point - executor_point for thing_point, executor_point in zip(thing_area, executor_area)])


class LocationShell(CommandShell):
    """
    Provides commands for manipulating objects inside Minecraft which have location.
    """

    @property
    def location(self):
        """
        Construct a location of this shell for a context. The location is ready to use in commands.
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
    def clone(self, other):
        """
        Clone this compound to another area.
        """
        shell = other.shell
        shell.context = self.context
        return "/clone {0} {1}".format(self.area, shell.location)

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
        other.shell.context = self.context
        return "/testforblocks {0} {1}".format(self.area, other.shell.location)

    def __eq__(self, other):
        """
        Check if this compound has the same blocks as other thing.
        :return: CommandSuspender
        """
        return self.testforblocks(other)


class MemoryShell(CompoundShell):
    def reset(self):
        """
        Set the memory to zero.
        """
        return self.fill(FALSE_BLOCK)


# A block has only a location. so it is very reasonable to have the same shell as the location shell.
BlockShell = LocationShell
