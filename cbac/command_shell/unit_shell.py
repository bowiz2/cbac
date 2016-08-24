from cbac.command_shell import CommandShell


class UnitShell(CommandShell):
    def set_callback(self, other):
        return self.wrapped.logic_cbas[-1].shell.set_callback(other)