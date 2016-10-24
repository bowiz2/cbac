"""
Holds the player class
"""
from cbac.core.command_shell.player_shell import PlayerShell
from cbac.core.utils import memoize


class Player(object):
    """
    Logical representation of a player in the minecraft world.
    Note, players cannot be added to a blockspace.
    """
    def __init__(self, name=None, random=False, all_players=False):
        """
        :param name: name of the player you want to represent. if None provided, you are representing the closest
        player to the object executing commands of the shell.
        """
        self.name = name
        self.random = random
        self.all_players = all_players
        assert not (self.random and self.all_players), "cannot be random and all players at the same time."

    @classmethod
    def random(cls):
        """
        represent the closest player.
        :return:
        """
        return Player(random=True)

    @classmethod
    def all_players(cls):
        """
        :return: Representation of all players
        """
        return Player(all_players=True)

    @property
    @memoize
    def shell(self):
        """
        :return: Minecraft command interface.
        """
        return PlayerShell(self)
