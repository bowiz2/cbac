"""
Holds the player shell.
"""
from cbac.core.command_shell.command_shell_base import CommandShell
from cbac.core.mc_command import TargetSelector, testfor


class PlayerShell(CommandShell):
    """
    Minecraft command interface.
    """
    @property
    def player(self):
        """
        :return: the player instance
        """
        return self.wrapped

    @property
    def base_selector(self):
        """
        :return: Base selector of the player.
        """
        if self.player.name or self.player.all_players:
            variable = 'a'
        elif self.player.random:
            variable = 'r'
        elif not self.player.name:
            variable = 'p'
        else:
            raise AssertionError("Invalid player instance configuration")

        return TargetSelector(variable, name=self.player.name)

    def test_exists(self):
        """
        Check if this player exists
        :return: lazy command
        """
        return testfor(self.base_selector)

    def test_coordinate(self, coordinate):
        """
        testfor if the player is at a specific coordinates.
        """
        selector = self.base_selector
        selector.coordinate = coordinate
        return testfor(selector)

    def test_rotation_vertical(self, minimum, maximum):
        """
        Test the rotation of the player in a range.
        :param minimum: minimal degree.
        :param maximum: maximal degree
        :return: testfor lazy command.
        """
        selector = self.base_selector
        selector.vertical_rotation = (minimum, maximum)
        return testfor(selector)

    def test_rotation_horizontal(self, minimum, maximum):
        """
                Test the rotation of the player in a range.
                :param minimum: minimal degree.
                :param maximum: maximal degree
                :return: testfor lazy command.
                """
        selector = self.base_selector
        selector.horizontal_rotation = (minimum, maximum)
        return testfor(selector)
