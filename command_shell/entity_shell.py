from .command_shell_base import CommandShell
from .decorator import command
from utils import format_realtive_location
from constants.block_id import TRUE_BLOCK, names
from constants.direction import vectors as direction_vectors



class EntityShell(CommandShell):
    @command()
    def kill(self):
        return self._join_command("/kill", self.wrapped.selector)

    @command()
    def execute(self, to_execute_command, location="~ ~ ~"):
        if not isinstance(to_execute_command, str):
            to_execute_command = to_execute_command()
        return self._join_command("/execute", self.wrapped.selector, location, to_execute_command)

    def activate(self):
        return self.execute("/setblock ~ ~ ~ {}".format(names[TRUE_BLOCK]))

    @command()
    def summon(self, location):
        """
        Summons an entity at a given location.
        :param location: The location you want to spawn the entity at.
        :return: CommandSuspender
        """
        entity = self.wrapped
        return self._join_command(
            "/summon",
            entity.mc_type,
            format_realtive_location(self.context.get_relative_location(location)),
            entity.parse_tags()
        )

    @command()
    def move(self, direction, times=1):
        direction_vector = direction_vectors[direction] * times
        return self._join_command("/tp", self.wrapped.selector, format_realtive_location(direction_vector))
