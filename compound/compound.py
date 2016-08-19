from command_shell import CompoundShell
from utils import memoize


class Compound(object):
    """Contains the blocks which are part of the compound. Later can be bound to a blockspace."""

    def __init__(self, blocks, isolated=False):
        self.blocks = blocks
        self.isolated = isolated

    @property
    @memoize
    def shell(self):
        return CompoundShell(self)



