"""
In this module there is an abstract representation of minecraft commands.
"""


# TODO: refactor creates condition to is_condition_creating. for now we use this because of a back comparability.


class MCCommand(object):
    """
    Represents a lazy initialized command.
    To use this command, you need to call the compile function.
    """

    def __init__(self, is_conditional=False, creates_condition=False, is_repeated=False):
        """
        :param is_conditional:  If the command is conditional, meaning it will execute only if the
        previously executed command was executed successfully.
        :param creates_condition: If the command creates condition for other commands. Meaning this command will
        force the next command inline to be conditional.
        This is mainly used for testforblock commands.
        """
        self.is_conditional = is_conditional
        self.creates_condition = creates_condition
        # If the command block holding this command will be repeated.
        self.is_repeated = is_repeated

    def compile(self):
        """
        Compile this mc command, for use in the minecraft world.
        :return: str
        :note: must be implemented.
        """
        assert False, "compile function was not implemented"


class SimpleCommand(MCCommand):
    """
    Represents a simple command which is not relied on some compile-time parameters.
    """

    def __init__(self, body, is_conditional=False, creates_condition=False):
        super(SimpleCommand, self).__init__(is_conditional, creates_condition)
        self._body = body

    def compile(self):
        """
        Create the simple command.
        :return:
        """
        return self._body


class EmptyCommand(MCCommand):
    """
    This is an empty command.
    """

    def compile(self):
        """
        :return: empty command string.
        """
        return "/say empty"


class LazyCommand(MCCommand):
    """
    This is a command which is lazy initialized and the uses a function which will be called with the supplied arguments
    in the compilation process.
    """

    def __init__(self, func, is_conditional=False, creates_condition=False, *args, **kwargs):
        assert all([isinstance(item, bool) for item in [is_conditional, creates_condition]]), "must be bool"
        super(LazyCommand, self).__init__(is_conditional, creates_condition)
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def compile(self):
        """
        Compile the command.
        :return:
        """
        return self.func(*self.args, **self.kwargs)


def factory(raw_command):
    """
    Convert a string into a simple command.
    :param raw_command: string representing mc command.
    :return: SimpleCommand.
    """
    assert isinstance(raw_command, str), "String must be a string."
    if raw_command is '':
        return EmptyCommand()

    conditional_operator = "?"
    condition_creation_operator = "!"
    command_start_prefix = "/"

    try:
        command_start_index = raw_command.index(command_start_prefix)
    except ValueError:
        raise MCCommandFactoryError(
            "Missing command start prefix '{0}' in the command '{1}'".format(command_start_prefix, raw_command))

    command_operators = raw_command[:command_start_index]
    conditional = conditional_operator in command_operators
    creates_condition = condition_creation_operator in command_operators
    for operator in command_operators:
        if operator not in [condition_creation_operator, conditional_operator]:
            raise MCCommandFactoryError("Invalid command operator '{0}'", operator)

    return SimpleCommand(raw_command[command_start_index:], conditional, creates_condition)


class MCCommandFactoryError(BaseException):
    """
    Thrown by the command factory.
    """
    pass


class TargetSelector(object):
    """
    A target selector variable identifies the broad category of targets to select. There are four variables: p r a and e
    """

    @classmethod
    def p(cls, *args, **kwargs):
        """
        @p
        Targets the nearest player. If there are multiple nearest players, caused by them being precisely the same
        distance away, the player who most recently joined the server is selected.
        Target selector arguments may be used to reduce the set of players from which the nearest player will be
        selected. For example, @p[team=Red] will target the nearest player on team Red even if there are other players
        closer.
        The c target selector argument can be used to increase the number of nearest players targeted
        (for example, @p[c=3] will target the three nearest players).
        When negative, c will reverse the order of targeting (for example, @p[c=-1]will target the farthest player).
        """
        return TargetSelector('p', *args, **kwargs)

    @classmethod
    def r(cls, *args, **kwargs):
        """
        Targets a random player (or entity with the type target selector argument).
        Target selector arguments may be used to reduce the set of players from which a random player will be targeted.
        For example, @r[team=Red] will only target a random player from team Red.
        The c target selector argument can be used to increase the number of random players targeted. For example,
        @r[c=3] will target three random players.
        When used without the type argument, @r always targets a random player. The type argument can be used to target
        non-player entities (for example, @r[type=Zombie] will target a random zombie, @r[type=!Player] will target
        a random non-player entity, @r[type=!Zombie] will target a random non-zombie, etc.).
        """
        return TargetSelector('r', *args, **kwargs)

    @classmethod
    def a(cls, *args, **kwargs):
        """
        Targets all players, including dead players. No other selector will find dead players.
        Target selector arguments may be used to reduce the set of players targeted. For example,
         @a[team=Red] will only target players on team Red.
        """
        return TargetSelector('a', *args, **kwargs)

    @classmethod
    def e(cls, *args, **kwargs):
        """
        Targets all entities (including players).
        Target selector arguments may be used to reduce the set of entities targeted. For example, @e[type=Cow] will
        only target cows.
        """
        return TargetSelector('e', *args, **kwargs)

    def __init__(self, variable, coordinate=(None, None, None), radius=(None, None),
                 volume_dimensions=(None, None, None), score_name=None,score_name_min=None, scoreboard_tag=None,
                 team_name=None, count=None, experience_level=(None, None), game_mode=None, name=None,
                 vertical_rotation=(None, None), horizontal_rotation=(None, None), entity_type=None, **kwargs):
        """
        :param variable:
        :param coordinate: x, y, z
        :param radius: r, rm (min, max)
        :param volume_dimensions: dx, dy, dz
        :param score_name: max score
        :param score_name_min: min score
        :param scoreboard_tag: tag
        :param team_name: team
        :param count: c
        :param experience_level: l, lm (min, max)
        :param game_mode: m
        :param name: entity name
        :param vertical_rotation: rx, rxm (max, min)
        :param horizontal_rotation: ry, rym (max, min)
        :param entity_type: type
        :param args:
        :param kwargs: you can use it to pass the minecraft notation
        """

        self.variable = variable
        self.coordinate = (
            kwargs.get('x', coordinate[0]),
            kwargs.get('y', coordinate[1]),
            kwargs.get('z', coordinate[2])
        )
        self.radius = (
            kwargs.get('r', radius[0]),
            kwargs.get('rm', radius[1])
        )
        self.volume_dimensions = (
            kwargs.get('dx', volume_dimensions[0]),
            kwargs.get('dy', volume_dimensions[1]),
            kwargs.get('dz', volume_dimensions[2])
        )

        self.score_name = score_name
        self.score_name_min = score_name_min
        self.scoreboard_tag = kwargs.get('tag', scoreboard_tag)
        self.team_name = kwargs.get('team', team_name)
        self.cout = kwargs.get('c', count)

        self.experience_level = (
            kwargs.get('l', experience_level[0]),
            kwargs.get('lm', experience_level[1])
        )

        self.game_mode = kwargs.get('m', game_mode)
        self.name = name

        self.vertical_rotation = (
            kwargs.get('rx', vertical_rotation[0]),
            kwargs.get('rxm', vertical_rotation[1])
        )

        self.horizontal_rotation = (
            kwargs.get('ry', horizontal_rotation[0]),
            kwargs.get('rym', horizontal_rotation[1])
        )

        self.entity_type = kwargs.get('type', entity_type)