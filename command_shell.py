def command(f):
    def _wrapper(*args, **kwargs):
        def _command_suspender():
            return f(*args, **kwargs)
        return _command_suspender
    return _wrapper


def area_string(area):
    area = map(location_string, area)
    return "{} {}".format(*area)


def location_string(location):
    return " ".join(map(str, location))


class CommandShell(object):
    """
    A command shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """
    def __init__(self, wrapped, blockspace):
        self. wrapped = wrapped
        self.blockspace = blockspace


class LocationShell(CommandShell):

    @property
    def location(self):
        return self.blockspace.get_location_of(self.wrapped)

    @command
    def testforblock(self, block_id, data_value=None, tags=None):

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
BlockShell = LocationShell


class CompoundShell(LocationShell):

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
