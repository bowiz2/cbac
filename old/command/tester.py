from command import Command
from area_command import AreaCommand


class TesterCommand(Command):
    """
    A command which tests something.
    """
    pass


class TestForBlock(TesterCommand):
    COMMAND_NAME = "testforblock"

    def __main__(self, target_location, tested_material):
        self.target_location = target_location
        self.material

class TestForBlocks(AreaCommand, TesterCommand):
    COMMAND_NAME = "testforblocks"

    def __init__(self, target_area, dest):
        super(Clone,self).__init__(target_area)
        self.dest = dest
    
    @property
    def params(self):
        for area_param in super(TestForBlocks, self).params:
            yield area_param
        x, y, z = dest
        yield "{} {} {}".format(x, y, z)