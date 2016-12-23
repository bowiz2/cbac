"""
In this module there is an abstract representation of minecraft commands.
"""
# TODO: refactor creates condition to is_condition_creating. for now we use this because of a back comparability.
from cbac.core import utils
from cbac.core.block import CommandBlock


def target_selector_inject(f):
    """
    injects the target selector of the command into the product.
    Used in MCCommand Classes
    :param f: compile function of the command
    :return: decorator.
    """

    def _wrapper(self, *args, **kwargs):
        product = f(self, *args, **kwargs)
        if self.target_selector:
            product = self.target_selector.inject(product)
        return product

    return _wrapper


class MCCommand(object):
    """
    Represents a lazy initialized command.
    To use this command, you need to call the compile function.
    """

    def __init__(self, is_conditional=False, creates_condition=False, is_repeated=False, target_selector=None):
        """
        :param is_conditional:  If the command is conditional, meaning it will execute only if the
        previously executed command was executed successfully.
        :param creates_condition: If the command creates condition for other commands. Meaning this command will
        force the next command inline to be conditional.
        This is mainly used for testforblock commands.
        """
        self.creates_condition = creates_condition
        # If the command block holding this command will be repeated.
        self.is_repeated = is_repeated
        self.target_selector = target_selector
        self.command_block = CommandBlock(command=self, conditional=is_conditional)

    @property
    def is_conditional(self):
        return self.command_block.conditional

    @is_conditional.setter
    def is_conditional(self, value):
        self.command_block.conditional = value

    @target_selector_inject
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

    @target_selector_inject
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
        return say("empty").compile()


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

    @target_selector_inject
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

    # Some prefixes of the commands.
    conditional_operator = "?"
    condition_creation_operator = "!"
    command_start_prefix = "/"

    # Get the end of the command prefixes and the start of the body of the command.
    try:
        command_start_index = raw_command.index(command_start_prefix)
    except ValueError:
        raise MCCommandFactoryError(
            "Missing command start prefix '{0}' in the command '{1}'".format(command_start_prefix, raw_command))

    # Extract the command operators such as '?' and '!'
    command_operators = raw_command[:command_start_index]
    # Check if the created command is conditional.
    is_conditional = conditional_operator in command_operators
    # Check if the created command creates condition.
    is_creates_condition = condition_creation_operator in command_operators

    # Check if all the command operators are valid.
    for operator in command_operators:
        if operator not in [condition_creation_operator, conditional_operator]:
            raise MCCommandFactoryError("Invalid command operator '{0}'", operator)

    # Return a simple command constructed with the parameters of the command.
    return SimpleCommand(raw_command[command_start_index:], is_conditional, is_creates_condition)


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

    def __init__(self, variable, coordinate=(None, None, None), radius=None, radius_min=None,
                 volume_dimensions=(None, None, None), score_name=None, score_name_min=None, scoreboard_tag=None,
                 team_name=None, count=None, experience_level=(None, None), game_mode=None, name=None,
                 vertical_rotation=(None, None), horizontal_rotation=(None, None), entity_type=None, **kwargs):
        """
        :param variable:
        :param coordinate: x, y, z
        :param radius: r
        :param radius_min: rm
        :param volume_dimensions: dx, dy, dz
        :param score_name: max score
        :param score_name_min: min score
        :param scoreboard_tag: tag
        :param team_name: team
        :param count: c
        :param experience_level: l, lm (min, max)
        :param game_mode: m
        :param name: entity name
        :param vertical_rotation: rx, rxm (min, max)
        :param horizontal_rotation: ry, rym (min, max)
        :param entity_type: type
        :param args:
        :param kwargs: you can use it to pass the minecraft notation
        """

        self.variable = variable
        # Extract the coordinate of the selected player.
        self.coordinate = (
            kwargs.get('x', coordinate[0]),
            kwargs.get('y', coordinate[1]),
            kwargs.get('z', coordinate[2])
        )

        self.radius = kwargs.get('r', radius)
        self.radius_min = kwargs.get('rm', radius_min)

        self.volume_dimensions = (
            kwargs.get('dx', volume_dimensions[0]),
            kwargs.get('dy', volume_dimensions[1]),
            kwargs.get('dz', volume_dimensions[2])
        )

        self.score_name = score_name
        self.score_name_min = score_name_min
        self.scoreboard_tag = kwargs.get('tag', scoreboard_tag)
        self.team_name = kwargs.get('team', team_name)
        self.count = kwargs.get('c', count)

        self.experience_level = (
            kwargs.get('l', experience_level[0]),
            kwargs.get('lm', experience_level[1])
        )

        self.game_mode = kwargs.get('m', game_mode)
        self.name = name

        self.vertical_rotation = (
            kwargs.get('rxm', vertical_rotation[0]),
            kwargs.get('rx', vertical_rotation[1])
        )

        self.horizontal_rotation = (
            kwargs.get('rym', horizontal_rotation[0]),
            kwargs.get('ry', horizontal_rotation[1])
        )

        self.entity_type = kwargs.get('type', entity_type)

    def inject(self, raw_command):
        """
        Inject the target selector into the compiled command string, useful in simple commands.
        """
        parts = raw_command.split(' ')
        inject_body = self.compile()
        return " ".join([parts[0], inject_body] + parts[1:])

    def compile(self):
        """
        :return: Compiled string of this selector (for example @a[x=10,y=20,z=30,r=4]) that can be used in commands.
        """

        # Translate the fields to their minecraft name.
        # The reason a tuple list is used instead of a dict is to preserve the order of the keys in the product.
        arguments = [
            ('x', self.coordinate[0]),
            ('y', self.coordinate[1]),
            ('z', self.coordinate[2]),
            ('r', self.radius),
            ('rm', self.radius_min),
            ('dx', self.volume_dimensions[0]),
            ('dy', self.volume_dimensions[1]),
            ('dz', self.volume_dimensions[2]),
            ('score_name', self.score_name),
            ('score_name_mim', self.score_name_min),
            ('tag', self.scoreboard_tag),
            ('team', self.team_name),
            ('c', self.count),
            ('l', self.experience_level[0]),
            ('lm', self.experience_level[1]),
            ('m', self.game_mode),
            ('name', self.name),
            ('rxm', self.vertical_rotation[0]),
            ('rx', self.vertical_rotation[1]),
            ('rym', self.horizontal_rotation[0]),
            ('ry', self.horizontal_rotation[1]),
            ('type', self.entity_type)
        ]
        # Filter out the empty fields and join the arguments in the correct format.
        arguments = ",".join(["{0}={1}".format(k, v) for k, v in arguments if v is not None])
        product = "@{0}[{1}]".format(self.variable, arguments)
        return product


def lazy_command(f):
    """
    Transforms a function into a lazy command
    """

    def _wrapper(*args, **kwargs):
        return LazyCommand(f, False, False, *args, **kwargs)

    return _wrapper


def lazy_command_condition(f):
    """
    Transforms a function into a lazy command which creates condition
    """

    def _wrapper(*args, **kwargs):
        return LazyCommand(f, False, True, *args, **kwargs)

    return _wrapper


from cbac.core.block import BlockID


def _join_command(*items):
    """
    Joins the items into a minecraft compatible format.
    """

    # TODO: implement test.
    def parse(obj):
        """
        Gets rid of null items, and formats dictionaries in the minecraft format.
        """
        if isinstance(obj, utils.Vector):
            return " ".join([str(i) for i in obj])
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                if value is not None:
                    new_dict[key] = value

            return str(new_dict).replace("'", "")

        return str(obj)

    return " ".join([parse(item) for item in items if item is not None])


@lazy_command_condition
def testfor(target_selector):
    """
    :param target_selector: what you are testing for.
    :return: Lazy command.
    """
    # Check if you can compile the target selector, or is it just a string.
    if hasattr(target_selector, 'compile'):
        target_selector = target_selector.compile()
    return "/testfor {}".format(target_selector)


@lazy_command
def say(message):
    """
    Display message to players
    :param message: message you want to display.
    """
    return "/say {0}".format(message)


# TODO: write tests for these commands.


@lazy_command
def clone(area, location, mask_mode="replace", clone_mode="normal", tile_name=None):
    """
    Clones blocks from region to another.
    :param area: from were to clone the blocks.
    :param location: Specifies the lower northwest corner (i.e., the smallest coordinates of each axis)
    of the destination region. May use tilde notation to specify a distance relative to the command's execution.
    :param mask_mode: Specifies whether to filter the blocks being cloned. Can be filtered, masked or replace.
    :param clone_mode: Specifies how to treat the source region. Can be force, move and normal.
    :param tile_name: Specifies the block id to copy when maskMode is set to filtered. Required by filtered mode.
    :return: Clone command suspender.
    """

    if not isinstance(area, str):
        area = utils.format_area(area)
    if not isinstance(location, str):
        location = utils.format_location(location)

    assert mask_mode in ["filtered", "masked", "replace"]
    assert clone_mode in ["force", "move", "normal"]

    if mask_mode == "filtered":
        assert tile_name is not None

    return _join_command("/clone", area, location, mask_mode, clone_mode, tile_name)


copy = clone


@lazy_command
def fill(area, block_id, data_value=None, block_handling=None, *options):
    """
    Fill an area with a block of a specific id.
    :param area: Area you want to fill
    :param block_id: id of the block
    :param data_value: data value of the block
    :param block_handling: fill mode
    :param options:
    """
    if not isinstance(area, str):
        area = utils.format_area(area)

    return _join_command("/fill", area, BlockID.names[block_id], data_value, block_handling, *options)


@lazy_command
def set_block(location, block_id, data_value=0, block_handling=None, tags=None):
    """
    Sets a block to a new block id with some more advanced options.
    """
    return _join_command("/setblock", location, BlockID.names[block_id], data_value, block_handling, tags)


@lazy_command_condition
def testforblock(location, block_id, data_value=0, tags=None):
    """
    Check if a block at this location is of a certain signature.
    """
    return _join_command("/testforblock", location, BlockID.names[block_id], data_value, tags)


__all__ = ["MCCommand", "SimpleCommand", "factory", "EmptyCommand", "testfor", "testforblock", "fill", "clone",
           "set_block", "say", "TargetSelector"]
