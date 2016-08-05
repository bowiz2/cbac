from block import Block
from constants.block_id import TRUE_BLOCK
from constants.block_id import names as block_names
from compound import Compound
# Selectors
NEAREST_PLAYER = '@p'
RANDOM_PLAYER = '@r'
ALL_PLAYERS = '@a'
ALL_ENTITIES = '@e'


def command(f):
    """
    Makes this function a suspended method. decorator
    """
    def _wrapper(*args, **kwargs):
        def _command_suspender():
            return f(*args, **kwargs)
        return _command_suspender
    return _wrapper


class CommandShell(object):
    """
    A command shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """
    def __init__(self, wrapped, blockspace, executor=None):
        """
        :param wrapped: The object which this command shell is wrapping.
        :param blockspace: The blockspace the wrapped object is located at.
        :param executor: the place from where the commands will be executed.
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

    @command
    def testforblock(self, block_id, data_value=None, tags=None):
        """
        Test if this location object is of the certain type.
        """
        return " ".join([str(item) for item in
                         ["/testforblock", self.location, block_names[block_id], data_value, tags]
                         if item is not None])

    @command
    def setblock(self, block_id, data_value=None, block_handling=None, tags=None):
        """
        Clone this compound to another area.
        """
        return " ".join([str(item) for item in
                         ["/setblock", self.location, block_names[block_id], data_value, block_handling, tags]
                         if item is not None])

    def activate(self):
        return self.setblock(TRUE_BLOCK)


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

    @command
    def clone(self, other):
        """
        Clone this compound to another area.
        """
        try:
            location = other.location
        except AttributeError:
            # TODO: clone to area.
            location = other

        return "/clone {} {}".format(self.area, location)

    @command
    def fill(self, block_id, data_value=None, block_handling=None, tags=None):
        """
        Clone this compound to another area.
        """

        return " ".join([str(item) for item in
                         ["/fill", self.area, block_names[block_id], data_value, block_handling, tags]
                         if item is not None])


def shell_factory(obj, blockspace):
    """
    Creates a shell for an object by its type. The shell is over a blockspace.
    """
    if isinstance(obj, Block):
        return LocationShell(obj, blockspace)
    if isinstance(obj, Compound):
        return CompoundShell(obj, blockspace)

# A block has only a location. so it is very reasonable to have the same shell as the location shell.
BlockShell = LocationShell
