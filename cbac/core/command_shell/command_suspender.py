"""
Holds Command Suspender
"""
from cbac.core.mc_command import LazyCommand


class CommandSuspender(LazyCommand):
    """
    Wraps a command generating function in a functor. Also holds meta-data of the generated command.
    such as its condition properties and the shell of that command.
    """

    def __init__(self, command_shell, command_function, *args, **kwargs):
        super(CommandSuspender, self).__init__(command_function, False, False, command_shell, *args, **kwargs)

    @property
    def command_shell(self):
        """
        The command command_shell which created the command.
        :return: CommandShell.
        """
        return self.args[0]

    @property
    def context(self):
        """
        The context of the shell which created this command, and by an extent the context of this command.
        """
        return self.command_shell.context

    @context.setter
    def context(self, value):
        self.command_shell.context = value

    def __call__(self):
        """
        Compiles the command
        """
        return self.compile()

    def __and__(self, other):
        """
        Return a list of this command and other command
        :param other: Other Command.
        This is used for the if statement sugar.
        :return: tuple of self and other.
        """
        assert isinstance(other, CommandSuspender), "Other must be a suspended command."
        assert self.creates_condition and other.creates_condition, "Both suspended commands must create condition"
        return self, other
