"""
Statements are syntactic sugar for the definition of units.
"""
import cbac.core.mc_command as mc_command
import copy
from cbac.core.utils import lrange

# TODO: move parsing logic inside the statement.
# TODO: implement wait statement


class Token(object):
    """
    This is the basic type of a statement and statement collection.
    """
    pass


    def parse(self, parser_instance):
        """
        Parse this statement in the parser.
        """
        pass


class Statement(Token):
    """
    Wraps a command or other statements
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.is_conditional = False


class Command(Statement):
    """
    Wraps a command
    """

    def __init__(self, raw_command):
        if isinstance(raw_command, str):
            raw_command = mc_command.factory(raw_command)
        super(Command, self).__init__(raw_command)

    def parse(self, parser_instance):
        """
        Parse logic
        """
        super(Command, self).parse(parser_instance)
        if self.is_conditional and isinstance(self.wrapped, mc_command.MCCommand):
            self.wrapped.is_conditional = True
        parser_instance.add_parsed(self.wrapped)


class StatementCollection(Token):
    """
    Wraps multiple statements.
    """

    def __init__(self, *statements):
        new_statements = []

        for statement in statements:
            if not isinstance(statement, Statement):
                statement = Command(statement)
            new_statements.append(statement)

        self.statements = new_statements

    def parse(self, parser_instance):
        """
        Parse logic.
        """
        super(StatementCollection, self).parse(parser_instance)
        # If the statement collection is conditional  each inner statement is conditional.
        if isinstance(self, Conditional):
            for statement in self.statements:
                statement.is_conditional = True
        self.statements.reverse()
        for statement in self.statements:
            parser_instance.parse_stack.append(statement)


class Jump(Statement):
    """jump to other location and return to the next logic cba after some logic."""

    @property
    def destination(self):
        """
        The destination of the jump.
        """
        return self.wrapped

    def parse(self, parser_instance):
        """
        Parse logic
        """
        super(Jump, self).parse(parser_instance)
        parser_instance.add_parsed(self.destination.activator.shell.activate())
        parser_instance.make_jump(self)


class MainLogicJump(Jump):
    """
    Main logic jump is a statement used in the main logic of a unit to jump to another item.
    """
    pass


class HardJump(Jump):
    """
    The jumps are not dynamic and are hard-wired.
    """
    # TODO: implement
    pass


class Conditional(StatementCollection):
    """
    All wrapped statements are now conditional.
    """
    pass


class PassParameters(Statement):
    """
    Pass parameters to the unit.
    """

    def __init__(self, unit, *parameters):
        super(PassParameters, self).__init__(unit)
        self.parameters = parameters

    @property
    def passed_unit(self):
        """
        The unit to which the params are passed.
        """
        return self.wrapped

    def parse(self, parser_instance):
        """
        parsing logic
        """
        super(PassParameters, self).parse(parser_instance)
        for param_id, parameter in enumerate(self.parameters):
            parser_instance.add_parsed(parameter.shell.copy(self.passed_unit.inputs[param_id]))


class Call(Statement):
    """
    Calls a unit
    """

    @property
    def called_unit(self):
        """
        The unit being called by this statements.
        """
        return self.wrapped


class STDCall(Call, PassParameters, MainLogicJump):
    """
    Copies parameter to function and then jumps to it.
    """
    pass


class Switch(Statement):
    """
    Switch statement.
    """

    def by(self, *cases):
        """
        Construct the statements for this switch
        """
        self.cases = cases
        return self


class _SwitchCase(Token):
    def __init__(self, to_compare):
        self.to_compare = to_compare

    def __call__(self, *body_statements):
        self.body_statements = body_statements
        return self


class _SwitchCaseSugar(object):
    """
    Singleton, just a get_item holder

    makes so I can use it like this

    case[thing](
        statement,
        statement,
    )
    """

    def __getitem__(self, item):
        return _SwitchCase(item)


case = _SwitchCaseSugar()


class InlineCall(Call, PassParameters):
    """
    Calls a unit without jump. Just pushes its commands to the commands of the current cba.
    """
    def parse(self, parser_instance):
        """
        Parse logic.
        """
        # TODO: support inline for jumpables units.
        PassParameters.parse(self, parser_instance)
        assert len(self.called_unit.logic_cbas) <= 1, "The inline-called function must not contain jumps"
        self.called_unit.is_inline = True
        for cba in self.called_unit.logic_cbas:
            for command in cba.commands:
                if self.is_conditional:
                    command.is_conditional = True
                parser_instance.add_parsed(copy.copy(command))


class If(Statement):
    """
    Usage:

    if(condition creating command).then(*commands which will be activated when the condition met).otherwise(...)

    of

    If (
        condition
    ).then(
        command_1,
        command_2,
        command_3
    ).otherwise(
        command_a,
        command_b
    )
    """

    def __init__(self, condition_commands):
        super(If, self).__init__(None)

        if not (isinstance(condition_commands, tuple) or isinstance(condition_commands, list)):
            condition_commands = [condition_commands]

        if isinstance(condition_commands, tuple):
            condition_commands = list(condition_commands)

        self.condition_commands = condition_commands
        self.condition_body = None
        self.otherwise_body = None

    def then(self, *statements):
        self.condition_body = Conditional(*statements)
        return self

    def otherwise(self, *statements):
        """
        Not used
        """
        self.otherwise_body = Conditional(*statements)
        return self

    def parse(self, parser_instance):
        """
        parse logic.
        """
        super(If, self).parse(parser_instance)
        if self.otherwise_body:
            parser_instance.parse_stack.append(self.otherwise_body)
            cb =  self.condition_commands[-1].command_block
            parser_instance.parse_stack.append(cb.shell.has_failed())

        parser_instance.parse_stack.append(self.condition_body)
        self.condition_commands.reverse()
        for command in self.condition_commands:
            parser_instance.parse_stack.append(command)


class TruthTable(Statement):
    """
    Aught to represent a truth table of ports.

    Format is as fallowes.
    yield TruthTable( [[in_a,  in_b,  in_c],  [out_a, out_b]],
                      "---------------------------------" // This is a decorator.
                      [[True,  True,  False], [True,  [True]],
                      [[False, False, False], [True,  False]],
                      [[True,  True,  False], [True,  True]])
    """

    @property
    def table(self):
        """
        This is the table which holds the rules for comprehention.
        :return: dict
        """
        return self.wrapped

    def parse(self, parser_instance):
        """
        Parse logic
        """
        super(TruthTable, self).parse(parser_instance)
        truth_table = self.table
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
                parser_instance.parse_stack.append(If(condition_cmds).then(*actions))

