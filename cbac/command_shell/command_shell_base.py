from cbac.utils import Vector

from . import ShellContext


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
        self.context = context

    @staticmethod
    def _join_command(*items):
        # TODO: implement test.
        def parse(obj):
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

# A block has only a location. so it is very reasonable to have the same command_shell as the location command_shell.
