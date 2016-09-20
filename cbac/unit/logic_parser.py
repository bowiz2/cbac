"""
This module parses the statement logic of a unit provided in its main logic commands generation method.
"""
from cbac.compound import CBA, Constant
from cbac.mc_command import MCCommand
from cbac.unit.statements import *
import cbac.config
import copy

# TODO: restructure as a compiler.

class ParseTreeNode(object):
    pass

class CommandCollection(list):
    #used for hashing.
    instance_count = 0

    def __init__(self, iterable=[]):
        self.my_id = CommandCollection.instance_count
        CommandCollection.instance_count+=1
        super(CommandCollection, self).__init__(iterable)

    def __hash__(self):
        return self.my_id

class JumpRef(object):
    """
    This is a jump reference which is left behind when a jump is made by some statement.
    """
    def __init__(self, before, destination, jumpback):
        """
        :param before: The node which have initiated the jump
        :param destination: the cba which is jumped to
        :param jumpback: The node which continue the parsing from now on.
        """
        self.before = before
        self.destination = destination
        self.jumpback = jumpback


class UnitLogicParser(object):
    """
    Parses the main logic of a unit.
    """

    def __init__(self):
        # Other compounds which were generated while parsing.
        self.other_compounds = []
        # The stack which is usd during parsing.
        self.parse_stack = []
        # holds all the jump refs
        self.jump_refs = []
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

        while len(pre_parsed_tokens) > 0:
            self.parse_stack.append(pre_parsed_tokens.pop(0))
            while len(self.parse_stack) > 0:
                token = self.parse_stack.pop()
                self.eat(token)

        cba_mapping = {}

        for command_collection in self.all_commands:
            cba = CBA(*command_collection)
            cba_mapping[command_collection] = cba
            logic_cbas.append(cba)

        for jump_ref in self.jump_refs:
            before_cba = cba_mapping[jump_ref.before]
            jumpback_cba = cba_mapping[jump_ref.jumpback]
            # TODO: auto include units which are jumped to if they have not been added to the parsed unit yet.
            # Use the callback reserved block to create the calback setting command for unit.
            before_cba.cb_callback_reserved.command = jump_ref.destination.shell.set_callback(jumpback_cba)

        return logic_cbas, self.other_compounds

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
        elif isinstance(statement, Debug):
            if cbac.config.DEBUG_BUILD:
                self.parse_stack.append(statement.wrapped)
        elif isinstance(statement, If):
            # Unwrap the if statement.
            self.parse_stack.append(statement.condition_body)
            statement.condition_commands.reverse()
            for command in statement.condition_commands:
                self.parse_stack.append(command)

        elif isinstance(statement, Switch):
            switch = statement
            for _case in statement.cases:
                constant = Constant(_case.to_compare)
                body = _case.body_statements
                self.parse_stack.append(If(switch.wrapped.shell == constant).then(*body))
                self.other_compounds.append(constant)

        elif isinstance(statement, InlineCall):
            # TODO: support inline for jumpables units.
            assert len(statement.called_unit.logic_cbas) <= 1, "The inline-called function must not contain jumps"
            statement.called_unit.is_inline = True
            for cba in statement.called_unit.logic_cbas:
                for command in cba.commands:
                    if statement.is_conditional:
                        command.is_conditional = True
                    self.add_parsed(copy.copy(command))
        elif isinstance(statement, MainLogicJump):
            prev_commands = self.commands
            new_commands = CommandCollection()
            jump_ref = JumpRef(prev_commands, statement.wrapped, self.commands)
            self.jump_refs.append(jump_ref)
            self.add_parsed(jump_ref.destination.shell.activate())
            self.all_commands.append(new_commands)
        else:
            assert False, "Invalid statement type."

    def add_parsed(self, command):
        """
        Add a parsed command to the command list.
        :param command:
        :return:
        """
        assert isinstance(command, MCCommand), "command must be of type MCCommand"
        self.commands.append(command)

"""
/say hey
/say bye
call adder
/say what



"""