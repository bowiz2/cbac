# Selectors
NEAREST_PLAYER = '@p'
RANDOM_PLAYER = '@r'
ALL_PLAYERS = '@a'
ALL_ENTITIES = '@e'


def command(f):
    """
    Makes this function a suspended method.
    """
    def _wrapper(*args, **kwargs):
        def _command_suspender():
            return f(*args, **kwargs)
        return _command_suspender
    return _wrapper


def area_string(area):
    """
    Convert area to the minecraft command representation.
    """
    area = map(location_string, area)
    return "{} {}".format(*area)


def location_string(location):
    """
    Converts a location into the minecraft representation.
    """
    return " ".join(map(str, location))


class CommandShell(object):
    """
    A command shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """
    def __init__(self, wrapped, blockspace, origin=None):
        """
        :param wrapped: The object which this command shell is wrapping.
        :param blockspace: The blockspace the wrapped object is located at.
        :param origin: the place from where the commands will be executed.
        """
        self. wrapped = wrapped
        self.blockspace = blockspace

    @command
    def raw(self, cmd):
        return cmd


class LocationShell(CommandShell):
    """
    Provides commands for manipulating objects inside Minecraft which have location.
    """
    @property
    def location(self):
        return self.blockspace.get_location_of(self.wrapped)

    def get_relative_location_of(self, thing):
        return self.location - self.blockspace.get_location_of(thing)

    @command
    def testforblock(self, block_id, data_value=None, tags=None):
        """
        Test if this location object is of the certain type.
        """
        return " ".join([str(item) for item in
                         ["/testforblock", location_string(self.location), block_id, data_value, tags]
                         if item is not None])

    @command
    def setblock(self, block_id, data_value=None, block_handling=None, tags=None):
        """
        Clone this compound to another area.
        """
        return " ".join([str(item) for item in
                         ["/setblock", location_string(self.location), block_id, data_value, block_handling, tags]
                         if item is not None])


class CompoundShell(LocationShell):
    """
    Provides commands for manipulating compounds inside Minecraft.
    """
    @property
    def area(self):
        # TODO: implement caching.
        return self.blockspace.get_area_of(self.wrapped)

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

        return "/clone {} {}".format(area_string(self.area), location_string(location))

    @command
    def fill(self, block_id, data_value=None, block_handling=None, tags=None):
        """
        Clone this compound to another area.
        """

        return " ".join([str(item) for item in
                         ["/fill", area_string(self.area), block_id, data_value, block_handling, tags]
                         if item is not None])


# A block has only a location. so it is very reasonable to have the same shell as the location shell.
BlockShell = LocationShell
