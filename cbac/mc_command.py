"""
In this module there is an abstract representation of minecraft commands.
"""
# TODO: refactor creates condition to is_condition_creating. for now we use this because of a back comparability.


class MCCommand(object):
    """
    Represents a lazy initialized command.
    To use this command, you need to call the compile function.
    """
    def __init__(self, is_conditional=False, creates_condition=False, is_repeated=False):
        """
        :param is_conditional:  If the command is conditional, meaning it will execute only if the
        previously executed command was executed successfully.
        :param creates_condition: If the command creates condition for other commands. Meaning this command will
        force the next command inline to be conditional.
        This is mainly used for testforblock commands.
        """
        self.is_conditional = is_conditional
        self.creates_condition = creates_condition
        # If the command block holding this command will be repeated.
        self.is_repeated = is_repeated

    def compile(self):
        """
        Compile this mc command, for use in the minecraft world.
        :return: str
        :note: must be implemented.
        """
        assert False, "compile function was not implemented"


class SimpleCommand(MCCommand):
    """
    Represents a simple command which is not relied on some compile-time parameters.
    """
    def __init__(self, body, is_conditional=False, creates_condition=False):
        super(SimpleCommand, self).__init__(is_conditional, creates_condition)
        self._body = body

    def compile(self):
        """
        Create the simple command.
        :return:
        """
        return self._body


class EmptyCommand(MCCommand):
    """
    This is an empty command.
    """
    def compile(self):
        """
        :return: empty command string.
        """
        return "/say empty"


class LazyCommand(MCCommand):
    """
    This is a command which is lazy initialized and the uses a function which will be called with the supplied arguments
    in the compilation process.
    """
    def __init__(self, func, is_conditional=False, creates_condition=False, *args, **kwargs):
        assert all([isinstance(item, bool) for item in [is_conditional, creates_condition]]), "must be bool"
        super(LazyCommand, self).__init__(is_conditional, creates_condition)
        self.args = args
        self.kwargs = kwargs
        self.func = func


    def compile(self):
        """
        Compile the command.
        :return:
        """
        return self.func(*self.args, **self.kwargs)


def factory(raw_command):
    """
    Convert a string into a simple command.
    :param raw_command: string representing mc command.
    :return: SimpleCommand.
    """
    assert isinstance(raw_command, str), "String must be a string."
    if raw_command is '':
        return EmptyCommand()

    conditional_operator = "?"
    condition_creation_operator = "!"
    command_start_prefix = "/"

    try:
        command_start_index = raw_command.index(command_start_prefix)
    except ValueError:
        raise MCCommandFactoryError("Missing command start prefix '{0}' in the command '{1}'".format(command_start_prefix, raw_command))

    command_operators = raw_command[:command_start_index]
    conditional = conditional_operator in command_operators
    creates_condition = condition_creation_operator in command_operators
    for operator in command_operators:
        if operator not in [condition_creation_operator, conditional_operator]:
            raise MCCommandFactoryError("Invalid command operator '{0}'", operator)

    return SimpleCommand(raw_command[command_start_index:], conditional, creates_condition)


class MCCommandFactoryError(BaseException):
    """
    Thrown by the command factory.
    """
    pass
