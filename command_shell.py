class CommandShell(object):
    """
    A command shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """
    def __init__(self, wrapped, blockspace):
        self. wrapped = wrapped
        self.blockspace = blockspace


class CompoundShell(CommandShell):

    @property
    def area(self):
        return self.blockspace.get_area_of(self.wrapped)


class BlockShell(CommandShell):
    @property
    def location(self):
        return self.blockspace.getlocation_of(self.wrapped)