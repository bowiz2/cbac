"""
This module parses the statement logic of a unit provided in its main logic commands generation method.
"""
from cbac.compound import CBA, Constant
from cbac.command_shell.command_suspender import CommandSuspender
from cbac.unit.statements import *



class Lazy(object):
    def __init__(self, target):
        self.target = target


class LazyCallbackSet(Lazy):
    pass


class LazyJump(Lazy):
    pass


def parse(statement_generators):
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
                        parse_statement_collection(parse_stack, token)

                    elif isinstance(token, Statement):
                        statement = token

                        if isinstance(statement, PassParameters):
                            for param_id, parameter in enumerate(statement.parameters):
                                add_parsed(parameter.shell.copy(statement.passed_unit.inputs[param_id]), commands)

                        if isinstance(statement, Command):
                            add_parsed(statement.wrapped, commands)

                        elif isinstance(statement, If):
                            # Unwrap the if statement.
                            parse_stack.append(statement.condition_commands)
                            parse_stack.append(statement.condition_body)

                        elif isinstance(statement, Switch):
                            switch = statement
                            for _case in statement.cases:
                                constant = Constant(_case.to_compare)
                                parse_stack.append(If(switch.wrapped.shell == constant).then(*_case.body_statements.statements))
                                other_compounds.append(constant)

                        elif isinstance(statement, InlineCall):
                            # TODO: support inline for jumpables units.
                            assert len(statement.called_unit.logic_cbas) == 1, "The inline-called function must not contain jumps"
                            statement.called_unit.is_inline = True
                            for command in statement.called_unit.logic_cbas[0].commands:
                                add_parsed(command, commands)
                        else:
                            assert False, "Invalid statement type."
                    else:
                        assert False, "Invalid token type"
                else:
                    parse_stack.append(Command(token))

    if len(commands) > 0:
        logic_cbas.append(CBA(*commands))

    # Repace the lazy inits with the real thing.
    for i, cba in enumerate(logic_cbas):
        for cb in cba.user_command_blocks:
            if isinstance(cb.command, Lazy):
                lazy_target = cb.command.target
                if isinstance(cb.command, LazyCallbackSet):
                    cb.command = lazy_target.shell.set_callback(logic_cbas[i + 1])
                if isinstance(cb.command, LazyJump):
                    cb.command = lazy_target.activator.shell.activate()

    # rewire the callbacks of all the cbac to be the actaull callback block of the last block.
    for cba in logic_cbas[:-1]:
        cba.cb_callback_reserved = logic_cbas[-1].cb_callback_reserved
    return logic_cbas, other_compounds


def add_parsed(command, commands):
    assert isinstance(command, str) or isinstance(command, CommandSuspender), "is not string or command suspender"
    commands.append(command)


def parse_statement_collection(parse_stack, token):
    # If the statement collection is conditional  each inner statement is conditional.
    if isinstance(token, Conditional):
        for statement in token.statements:
            statement.is_conditional = True
    token.statements.reverse()
    for statement in token.statements:
        parse_stack.append(statement)

