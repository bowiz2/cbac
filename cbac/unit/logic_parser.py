"""
This module parses the statement logic of a unit provided in its main logic commands generation method.
"""
from cbac.compound import CBA, Constant
from cbac.command_shell.command_suspender import CommandSuspender
from cbac.unit.statements import *


def parse(statement_generators):
    """
    Parse the statements in the statement generator.
    """
    logic_cbas = []
    commands = []
    other_compounds = []

    parse_stack = []

    for command_generator in statement_generators:
        # Parse Statements
        pre_parsed_tokens = list(command_generator)

        while len(pre_parsed_tokens) > 0:
            parse_stack.append(pre_parsed_tokens.pop(0))

            while len(parse_stack) > 0:

                token = parse_stack.pop()
                # Copy Parameters and rename the statemnt to a main logic jump
                if isinstance(token, Token):
                    if isinstance(token, StatementCollection):
                        parse_statement_collection(token, parse_stack)

                    elif isinstance(token, Statement):
                        parse_statement(token, parse_stack, commands, other_compounds)
                    else:
                        assert False, "Invalid token type"
                else:
                    parse_stack.append(Command(token))

    if len(commands) > 0:
        logic_cbas.append(CBA(*commands))

    return logic_cbas, other_compounds


def parse_statement_collection(statement_collection, parse_stack):
    """
    Parses the statement collection token
    :param statement_collection: StatementCollection
    :param parse_stack: the parse stack to which the results will be pushed.
    """
    # If the statement collection is conditional  each inner statement is conditional.
    if isinstance(statement_collection, Conditional):
        for statement in statement_collection.statements:
            statement.is_conditional = True
    statement_collection.statements.reverse()
    for statement in statement_collection.statements:
        parse_stack.append(statement)


def parse_statement(statement, parse_stack, commands, other_compounds):
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
            add_parsed(parameter.shell.copy(statement.passed_unit.inputs[param_id]), commands)
    if isinstance(statement, Command):
        add_parsed(statement.wrapped, commands)

    elif isinstance(statement, If):
        # Unwrap the if statement.
        parse_stack.append(statement.condition_body)
        statement.condition_commands.reverse()
        for command in statement.condition_commands:
            parse_stack.append(command)

    elif isinstance(statement, Switch):
        switch = statement
        for _case in statement.cases:
            constant = Constant(_case.to_compare)
            body = _case.body_statements
            parse_stack.append(If(switch.wrapped.shell == constant).then(*body))
            other_compounds.append(constant)

    elif isinstance(statement, InlineCall):
        # TODO: support inline for jumpables units.
        assert len(statement.called_unit.logic_cbas) == 1, "The inline-called function must not contain jumps"
        statement.called_unit.is_inline = True
        for command in statement.called_unit.logic_cbas[0].commands:
            add_parsed(command, commands)
    else:
        assert False, "Invalid statement type."


def add_parsed(command, commands):
    assert isinstance(command, str) or isinstance(command, CommandSuspender), "is not string or command suspender"
    commands.append(command)


