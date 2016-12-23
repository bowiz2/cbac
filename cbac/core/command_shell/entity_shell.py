"""
Holds Entity Shell
"""
from cbac.core.command_shell.command_shell_base import CommandShell
from cbac.core.command_shell.decorator import command
from cbac.core.block import BlockID
from cbac.core.utils import Vector
from cbac.core.utils import format_relative_location, format_location, format_relative_area, absolute_area, format_area
from cbac.core.mc_direction import MCDirection


class EntityShell(CommandShell):
    """
    Wraps the mcentity object and provides command interface for it.
    """

    @command()
    def kill(self):
        """
        Kills this mcentity
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
    def summon(self, location=Vector(0, 0, 0)):
        """
        Summons an mcentity at a given location.
        :param location: The location you want to spawn the mcentity at.
        :return: Summon command.
        """
        entity = self.wrapped
        return self._join_command(
            "/summon",
            entity.mc_type,
            format_relative_location(self.context.get_relative_location(location)),
            entity.parse_tags()
        )

    @command()
    def move(self, direction, distance=1):
        """
        Moves this mcentity in a direction by a distance
        :param direction: The direction to move the mcentity.
        :param distance: How far to move the mcentity.
        :return: Tp command.
        """
        direction_vector = MCDirection.vectors[direction] * distance
        return self._join_command("/tp", self.wrapped.selector, format_relative_location(direction_vector))

    @command()
    def tp(self, thing, break_point=False):
        """
        teleport this pivot to a locatable item
        :param location:
        :return:
        """
        location = self.context.get_absolute_location(thing)
        if break_point:
            location += Vector(0, 1, 0)
        return self._join_command("/tp", self.wrapped.selector, format_relative_location(location))

    def activate(self):
        """
        Set the block at which this mcentity is standing as true block.
        :return: Execute command.
        """
        return self.execute("/setblock ~ ~ ~ {}".format(BlockID.names[BlockID.TRUE_BLOCK]))


class PivotShell(EntityShell):
    """
    Provide command interface for the pivot, mainly to clone stuff to and from a temp location.
    """

    # TODO: Write very good documentation.
    @command()
    def store_to_temp(self, area, temp_location=(0, 0, 0)):
        """
        Save to temp location the area at the current position of the pivot.
        :param area: Can be a tuple of points or an object which has area and can be gotten from a blockspace.
        :param temp_location: The location to which save the area.
        :return:
        """
        # in case the object has an area and is not an area by itself.
        if not isinstance(area, tuple):
            area = self.context.blockspace.get_area_of(area)
            area = absolute_area(area)

        return self.execute(self._join_command(
            "/clone",
            format_relative_area(area),
            format_location(temp_location)
        ))()

    @command()
    def load_from_temp(self, area, temp_location=(0, 0, 0)):
        """
        :param area:
        :param temp_location:
        :return:
        """
        if not isinstance(area, tuple):
            area = self.context.blockspace.get_area_of(area)
            area = absolute_area(area)
        temp_location = Vector(*temp_location)
        temp_area = [Vector(*point) + temp_location for point in area]
        return self.execute(self._join_command(
            "/clone",
            format_area(temp_area),
            format_relative_location((0, 0, 0))
        ))()
