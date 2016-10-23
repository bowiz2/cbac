"""
Holds abstract Command shell.
"""
from cbac.core.command_shell.shell_context import ShellContext

from cbac.core.utils import Vector


class CommandShell(object):
    """
    A command command_shell is a wrapper object which wrapes some object,
    and provides some functionality which later can be used with command blocks.
    operates on a block space.
    """

    def __init__(self, wrapped, context=(None, None)):
        """
        :param wrapped: The object which this command command_shell is wrapping.
        :param context
        """
        self.wrapped = wrapped
        # Coupling.
        if not isinstance(context, ShellContext):
            context = ShellContext(*context)
        # This is the original context
        self._real_context = context
        self.context = context

    @staticmethod
    def _join_command(*items):
        """
        Joins the items into a minecraft compatible format.

        """
        # TODO: implement test.
        def parse(obj):
            """
            Gets rid of null items, and formats dictionaries in the minecraft format.
            """
            if isinstance(obj, Vector):
                return " ".join([str(i) for i in obj])
            if isinstance(obj, dict):
                new_dict = {}
                for key, value in obj.items():
                    if value is not None:
                        new_dict[key] = value

                return str(new_dict).replace("'", "")

            return str(obj)

        return " ".join([parse(item) for item in items if item is not None])
