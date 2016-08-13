from .decorator import command
from . import LocationShell

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
