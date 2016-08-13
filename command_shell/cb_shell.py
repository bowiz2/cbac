from .location_shell import BlockShell
from .decorator import command


class CommandBlockShell(BlockShell):
    """
    Command block shell is a shell which can only be used with command blocks.
    """

    @command()
    def change_command(self, new_command):
        if not isinstance(new_command, str):
            new_command.context = self.context
            new_command = new_command()
        else:
            new_command = new_command
        return self.setblock(
            self.wrapped.block_id,
            self.wrapped.data_value,
            "replace",
            {"Command": new_command, "auto": 1 if self.wrapped.always_active else 0}
        )()
