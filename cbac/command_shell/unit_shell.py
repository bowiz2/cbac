"""
Holds Unit shell.
"""
from cbac.command_shell import CommandShell


class UnitShell(CommandShell):
    """
    Wraps a unit object with command interface.
    """
    def set_callback(self, other):
        """
        Set the callback of this unit to another dynamic calling object.
        """
        return self.wrapped.logic_cbas[-1].shell.set_callback(other)
