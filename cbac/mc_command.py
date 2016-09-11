"""
In this module there is an abstract representation of minecraft commands.
"""


class MCCommand(object):
    """
    Represents a lazy initialized command.
    To use this command, you need to call the compile function.
    """
    def __init__(self, is_conditional=False):
        self.is_conditional = is_conditional

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
    def __init__(self, body, is_conditional=False):
        super(SimpleCommand, self).__init__(is_conditional)
        self._body = body

    def compile(self):
        """
        Create the simple command.
        :return:
        """
        return self._body
