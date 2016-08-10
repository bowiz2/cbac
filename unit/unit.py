import command_shell
from block import Block
from compound import Compound


class Unit(object):
    def __init__(self, blockspace):
        self.blockspace = blockspace
        self.compounds = dict()

    def shell(self, item):
        if isinstance(item, Block):
            return command_shell.LocationShell(item, self.blockspace)
        if isinstance(item, Compound):
            return command_shell.CompoundShell(item, self.blockspace)
