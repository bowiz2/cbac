"""
Holds Entity Shell
"""
from cbac.constants.block_id import TRUE_BLOCK, names
from cbac.constants.mc_direction import vectors as direction_vectors
from cbac.constants.mc_direction import EAST
from cbac.utils import format_realtive_location, format_location
from cbac.command_shell.command_shell_base import CommandShell
from cbac.command_shell.decorator import command
from utils import Vector


class EntityShell(CommandShell):
    """
    Wraps the entity object and provides command iterface for it.
    """
    @command()
    def kill(self):
        """
        Kills this entity
        :return: Kill command.
        """
        return self._join_command("/kill", self.wrapped.selector)

    @command()
    def execute(self, to_execute_command, location="~ ~ ~"):
        """
        Executes a command on behalf of one or more other entities, with originating permissions,
            optionally on condition that a single-block /testforblock-style check passes.
        :param to_execute_command: Specifies the command to be run. Must be a valid command.
        :param location: Specifies the position from which to run the command.
        :return: Execute command.
        """
        if not isinstance(to_execute_command, str):
            to_execute_command = to_execute_command()
        return self._join_command("/execute", self.wrapped.selector, location, to_execute_command)

    @command()
    def summon(self, location):
        """
        Summons an entity at a given location.
        :param location: The location you want to spawn the entity at.
        :return: Summon command.
        """
        entity = self.wrapped
        return self._join_command(
            "/summon",
            entity.mc_type,
            format_realtive_location(self.context.get_relative_location(location)),
            entity.parse_tags()
        )

    @command()
    def move(self, direction, distance=1):
        """
        Moves this entity in a direction by a distance
        :param direction: The direction to move the entity.
        :param distance: How far to move the entity.
        :return: Tp command.
        """
        direction_vector = direction_vectors[direction] * distance
        return self._join_command("/tp", self.wrapped.selector, format_realtive_location(direction_vector))

    # TODO: standardise point of reference.
    def clone_to_point_of_reference(self, word_size, point_of_reference=(0, 0, 0), word_direction=EAST):
        """
        Clone a word size area to the point of reference which is the location (0,0,0) in this minecraft world
        :return: CommandSuspender
        :note: Sees use in the RAM standard unit.
        """
        return self.execute(self._join_command(
            "/clone",
            format_realtive_location((0, 0, 0)),
            format_realtive_location(direction_vectors[word_direction] * word_size),
            format_location(point_of_reference)
        ))

    def load_from_point_of_reference(self, word_size, point_of_reference=(0, 0, 0), word_direction=EAST):
        """
        clone  from the point of reference area to the location at which the entity is staying.
        "Point of reference" is the location (0,0,0) in this minecraft world.
        :return: CommandSuspender
        :note: Sees use in the RAM standard unit.
        """
        point_of_reference = Vector(*point_of_reference)
        return self.execute(self._join_command(
            "/clone",
            format_location(point_of_reference),
            format_location(point_of_reference + (direction_vectors[word_direction] * word_size)),
            format_realtive_location((0, 0, 0))

        ))

    def activate(self):
        """
        Set the block at which this entity is standing as true block.
        :return: Execute command.
        """
        return self.execute("/setblock ~ ~ ~ {}".format(names[TRUE_BLOCK]))
