class CommandSuspender(object):
    def __init__(self, command_shell, command_function, *args, **kwargs):
        # The command command_shell which created the command.
        self.command_shell = command_shell
        # The actual command function which was suspended.
        self.command_function = command_function
        # The args which will be used when the command function will be resumed
        self.args = args
        self.kwargs = kwargs
        # If the command creates conditioning for other commands. testforblock for example, creates conditioning.
        self.creates_condition = False
        # If the command is executed only if it is met with a condition of previusly executed command block.
        self.is_conditional = False

    def __call__(self):
        return self.command_function(self.command_shell, *self.args, **self.kwargs)

    def __and__(self, other):
        """
        Return a list of this command and other command
        :param other: Other Command.
        :return: tuple of self and other.
        """
        return self, other
