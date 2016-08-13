from . import CompoundShell
from .decorator import command

class CBAShell(CompoundShell):

    @command()
    def set_callback(self, other):

        self.wrapped.cb_callback_reserved.shell.context = self.context

        other.shell.context.blockspace = self.context.blockspace
        other.activator.shell.context.blockspace = self.context.blockspace

        other.shell.context.executor = self.wrapped.cb_callback_reserved
        other.activator.shell.context.executor =self.wrapped.cb_callback_reserved
        return self.wrapped.cb_callback_reserved.shell.change_command(other.activator.shell.activate())()
