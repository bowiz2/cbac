from cbac.core.command_shell import CompoundShell

from cbac.core.utils import memoize


class Compound(object):
    """Contains the blocks which are part of the compound. Later can be bound to a blockspace."""

    def __init__(self, isolated=False):
        self.isolated = isolated

    @property
    @memoize
    def blocks(self):
        """
        :return: collection of blocks which compose this compound.
        """
        return []

    @property
    @memoize
    def shell(self):
        """
        :return: Minecraft command interface for the compound
        """
        return CompoundShell(self)
