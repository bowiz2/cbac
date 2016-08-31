"""
Holds decorators for the command shell logical components.
"""
from . import CommandSuspender


def command(creates_condition=None):
    """
    :param creates_condition: whenever this command creates condition.
    :return: command decorator.
    """

    def command_decorator(f):
        """
        Makes this function a suspended method. decorator
        """

        def _wrapper(self, *args, **kwargs):
            sus = CommandSuspender(self, f, *args, **kwargs)
            sus.creates_condition = creates_condition
            return sus

        return _wrapper

    return command_decorator
