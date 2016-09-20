"""
Holds Command Block Shell for the Minecraft command block.
"""
from cbac.command_shell.decorator import command
from cbac.command_shell.location_shell import BlockShell


class CommandBlockShell(BlockShell):
    """
    Command block shell is a shell which can only be used with command blocks.
    """

    @command()
    def change_command(self, new_command):
        """
        Change the command of this command block.
        :param new_command: The command which will take the place of the all command.
        :return: CommandSuspender
        """
        if not isinstance(new_command, str):
            new_command.context = self.context
            new_command = new_command.compile()
        else:
            new_command = new_command
        return self.setblock(
            self.wrapped.block_id,
            self.wrapped.data_value,
            "replace",
            {"Command": new_command, "auto": 1 if self.wrapped.always_active else 0}
        )()

    @command(True)
    def has_succeeded(self):
        """
        Check if this command block succeeded with the last execution of his command.
        :return: CommandSuspender
        """
        return self.testforblock(self.wrapped.block_id, self.wrapped.data_value, {"SuccessCount": 1})()

    def set_call(self, target):
        """
        Makes that this block will activate target block.
        :return: CommandSuspender
        """

        return self.change_command(target.shell.activate())