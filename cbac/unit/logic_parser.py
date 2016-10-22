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
            if isinstance(token, StatementCollection):
                self.parse_statement_collection(token)

            elif isinstance(token, Statement):
                self.parse_statement(token)
            else:
                assert False, "Invalid token type"
        else:
            self.parse_stack.append(Command(token))

    def parse_statement_collection(self, statement_collection):
        """
        Parses the statement collection token
        :param statement_collection: StatementCollection
        """
        # If the statement collection is conditional  each inner statement is conditional.
        if isinstance(statement_collection, Conditional):
            for statement in statement_collection.statements:
                statement.is_conditional = True
        statement_collection.statements.reverse()
        for statement in statement_collection.statements:
            self.parse_stack.append(statement)

    def parse_statement(self, statement):
        """
        Parse a statement and push thre mi-results to the parse stack, the command results to the command list
        and the generated compounds in the other_compounds list.
        :param statement: statement you want to parse.
        :param parse_stack:
        :param commands:
        :param other_compounds:
        :return:
        """
        if isinstance(statement, PassParameters):
            for param_id, parameter in enumerate(statement.parameters):
                self.add_parsed(parameter.shell.copy(statement.passed_unit.inputs[param_id]))
        if isinstance(statement, Command):
            if statement.is_conditional and isinstance(statement.wrapped, MCCommand):
                statement.wrapped.is_conditional = True
            self.add_parsed(statement.wrapped)
        elif isinstance(statement, If):
            # Unwrap the if statement.
            self.parse_stack.append(statement.condition_body)
            statement.condition_commands.reverse()
            for command in statement.condition_commands:
                self.parse_stack.append(command)

        elif isinstance(statement, InlineCall):
            # TODO: support inline for jumpables units.
            assert len(statement.called_unit.logic_cbas) <= 1, "The inline-called function must not contain jumps"
            statement.called_unit.is_inline = True
            for cba in statement.called_unit.logic_cbas:
                for command in cba.commands:
                    if statement.is_conditional:
                        command.is_conditional = True
                    self.add_parsed(copy.copy(command))

        elif isinstance(statement, Jump):
            self.add_parsed(statement.destination.activator.shell.activate())
            self.make_jump(statement)

        elif isinstance(statement, TruthTable):
            truth_table = statement.table
            # Sort out sugar strings.
            truth_table = filter(lambda x: not isinstance(x, str), truth_table)

            assert len(truth_table) > 1, "Truth table must contain at-least one port row and one value row."

            in_ports, out_ports = truth_table[0]

            in_states = []
            out_states = []

            for state_pair in truth_table[1:]:
                in_state, out_state = state_pair
                in_states.append(in_state)
                out_states.append(out_state)

            assert all(len(in_ports) is len(in_state) for in_state in in_states), \
                "in state must be equal to in ports"
            assert all(len(out_ports) is len(out_state) for out_state in out_states), \
                "out state must be equal to out ports"

            ports_dict = {}

            for i, port in enumerate(in_ports):
                ports_dict[port] = [state[i] for state in in_states]

            for i, port in enumerate(out_ports):
                ports_dict[port] = [state[i] for state in out_states]

            for i in lrange(in_states):
                actions = [output_port.shell.activate() for output_port in out_ports if ports_dict[output_port][i]]
                if len(actions) > 0:
                    condition_cmds = []
                    for input_port in in_ports:
                        if ports_dict[input_port][i]:
                            condition_cmds.append(input_port.shell == True)
                        else:
                            condition_cmds.append(input_port.shell == False)
                    self.parse_stack.append(If(condition_cmds).then(*actions))

        else:
            assert False, "'{}' Is an invalid statement type.".format(statement.__class__.__name__)

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
                origin_cba.cb_callback_reserved.command = listener.activator.shell.activate()
                yield listener

    def add_parsed(self, command):
        """
        Add a parsed command to the command list.
        :param command:
        :return:
        """
        assert isinstance(command, MCCommand), "command must be of type MCCommand"
        self.commands.append(command)
