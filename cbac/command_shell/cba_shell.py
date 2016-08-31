"""
Holds Command Block Array shell.
"""
from . import CompoundShell
from .decorator import command


class CBAShell(CompoundShell):
    """
    Wraps Command block array object, and provides a command interface for it which command block objects can use.
    """
    @command()
    def set_callback(self, other):
        """
        Set the callback of a command block array to another command block array.
        :param other: CBA
        :return: CommandSuspender
        """
        self.wrapped.cb_callback_reserved.shell.context = self.context

        other.shell.context.blockspace = self.context.blockspace
        other.activator.shell.context.blockspace = self.context.blockspace

        other.shell.context.executor = self.wrapped.cb_callback_reserved
        other.activator.shell.context.executor = self.wrapped.cb_callback_reserved
        return self.wrapped.cb_callback_reserved.shell.change_command(other.activator.shell.activate())()
