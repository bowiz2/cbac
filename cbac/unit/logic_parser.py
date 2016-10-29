"""
This module parses the statement logic of a unit provided in its main logic commands generation method.
"""
import copy

from cbac.core.utils import lrange

from cbac.core import utils
from cbac.unit.statements import *
from cbac.core.compound import CBA
from cbac.core.mc_command import MCCommand


# TODO: restructure as a compiler.


class CommandCollection(list):
    """
    A collection of commands which can be hashed.
    """
    # used for hashing.
    instance_count = 0

    def __init__(self, iterable=[]):
        self.my_id = CommandCollection.instance_count
        CommandCollection.instance_count += 1
        super(CommandCollection, self).__init__(iterable)

    def __hash__(self):
        return self.my_id


class UnitLogicParser(object):
    """
    Parses the main logic of a unit.
    """

    # TODO: refactor
    def __init__(self):
        # TODO: organize.
        # Other compounds which were generated while parsing.
        self.other_compounds = []
        # Other Units which were generated while parsing. # TODO: merge other units with listeners
        self.other_units = []
        # Listener units which were generated while parsing.
        self.listeners = []
        # contains all the jumps which are aought to be made. TODO: rewrite
        self.jumps = []
        # The stack which is usd during parsing.
        self.parse_stack = []
        # list of all the commands in their seperated thign.
        # TODO: give better name.
        self.all_commands = [CommandCollection()]

    @property
    def commands(self):
        """
        :return: Last cba which we are working on.
        """
        return self.all_commands[-1]

    def parse(self, tokens):
        """
        Parse the statements in the statement generator.
        """
        self.all_commands = [CommandCollection()]
        self.other_compounds = []
        self.parse_stack = []

        logic_cbas = []

        # Parse Statements
        pre_parsed_tokens = list(tokens)
        pre_parsed_tokens = utils.flatten(pre_parsed_tokens, 2)

        while len(pre_parsed_tokens) > 0:
            self.parse_stack.append(pre_parsed_tokens.pop(0))
            while len(self.parse_stack) > 0:
                token = self.parse_stack.pop()
                self.eat(token)

        cba_mapping = {}
        if len(self.commands) == 0:
            self.commands.append(mc_command.factory("/say last"))

        for command_collection in self.all_commands:
            cba = CBA(*command_collection)
            cba_mapping[command_collection] = cba
            logic_cbas.append(cba)

        self.listeners += list(self.generate_listeners(logic_cbas))

        return logic_cbas, self.other_compounds, self.listeners + self.other_units

    def eat(self, token):
        """
        Eat a token and process it.
        :param token: Token you want to process.
        :return:
        """
        # Copy Parameters and rename the statemnt to a main logic jump
        if isinstance(token, Token):
            token.parse(self)
        else:
            self.parse_stack.append(Command(token))

    def make_jump(self, jump_statement):
        """
        Create a jump.
        Will be processed later when the logic cbas will be constructed.
        :param jump_statement: The statement which caused the jump.
        """
        self.jumps.append(jump_statement)
        new_commands = CommandCollection()
        self.all_commands.append(new_commands)

    def generate_listeners(self, logic_cbas):
        """
        generate all the needed preparation for a jump to work
        :return: generated units which needed for the jump to work.
        """
        # TODO: fix that hack
        from cbac.std_unit.listner_unit import IsNotActiveListener
        for i, jump in enumerate(self.jumps):
            # The cba from which the jump was made
            origin_cba = logic_cbas[i]
            landing_cba = logic_cbas[i + 1]
            if isinstance(jump, MainLogicJump):
                listener = IsNotActiveListener(jump.destination.activator, landing_cba)
                # Activate the listener.
                origin_cba.cb_reserved.command = listener.activator.shell.activate()
                yield listener

    def add_parsed(self, command):
        """
        Add a parsed command to the command list.
        :param command:
        :return:
        """
        assert isinstance(command, MCCommand), "command must be of type MCCommand instead got {0}".format(
            command.__class__.__name__)
        self.commands.append(command)
