"""
This module parses the statement logic of a unit provided in its main logic commands generation method.
"""
from cbac.compound import CBA, Constant
from cbac.command_shell.command_suspender import CommandSuspender
from cbac.unit.statements import *


class UnitLogicParser(object):
    """
    Parses the main logic of a unit.
    """

    def __init__(self):
        # List of parsed commands.
        self.commands = []
        # Other compounds which were generated while parsing.
        self.other_compounds = []
        # The stack which is usd during parsing.
        self.parse_stack = []

    def parse(self, tokens):
        """
        Parse the statements in the statement generator.
        """
        self.commands = []
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

        if len(self.commands) > 0:
            logic_cbas.append(CBA(*self.commands))

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
            if statement.is_conditional and isinstance(statement.wrapped, CommandSuspender):
                statement.wrapped.is_conditional = True
            self.add_parsed(statement.wrapped)

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
            assert len(statement.called_unit.logic_cbas) == 1, "The inline-called function must not contain jumps"
            statement.called_unit.is_inline = True
            for command in statement.called_unit.logic_cbas[0].commands:
                if statement.is_conditional:
                    command.is_conditional = True
                self.add_parsed(command)
        else:
            assert False, "Invalid statement type."

    def add_parsed(self, command):
        """
        Add a parsed command to the command list.
        :param command:
        :return:
        """
        assert isinstance(command, str) or isinstance(command, CommandSuspender), "is not string or command suspender"
        self.commands.append(command)


