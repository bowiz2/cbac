from cbac.command_shell import CompoundShell
from cbac.utils import memoize


class Compound(object):
    """Contains the blocks which are part of the compound. Later can be bound to a blockspace."""

    def __init__(self, isolated=False):
        self.isolated = isolated

    @property
    @memoize
    def blocks(self):
        return []

    @property
    @memoize
    def shell(self):
        return CompoundShell(self)
