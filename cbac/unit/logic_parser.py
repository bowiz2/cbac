"""
This module parses the statement logic of a unit provided in its main logic commands generation method.
"""
from cbac.unit.statements import Statement, MainLogicJump, Conditional, STDCall
from compound import CBA


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

    for command_generator in statement_generators:
        # Parse Statements
        for statement in command_generator:
            # wrap the command in a statement.
            if not isinstance(statement, Statement):
                statement = Statement(statement)

            # Copy Parameters and rename the statemnt to a main logic jump
            if isinstance(statement, STDCall):
                for param_id, parameter in enumerate(statement.parameters):
                    commands.append(parameter.shell.copy(statement.called_unit.inputs[param_id]))
                statement = MainLogicJump(statement.called_unit)

            if isinstance(statement, Conditional):
                for command in statement.commands:
                    command.is_conditional = True
                    commands.append(command)
            elif isinstance(statement, MainLogicJump):
                # Lazy init some stuff.
                commands.append(LazyCallbackSet(statement.wrapped))
                commands.append(LazyJump(statement.wrapped))
                logic_cbas.append(CBA(*commands))
                commands = []
            else:
                # regular statement
                commands.append(statement.wrapped)

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
    return logic_cbas