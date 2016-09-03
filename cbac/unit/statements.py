"""
Statements are syntactic sugar for the definition of units.
"""


# TODO: implement switch statement.


class Statement(object):
    """
    Wraps a command or other statements
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped


class Command(Statement):
    """
    Wraps a command
    """
    pass


class StatementCollection(object):
    """
    Wraps multiple statements.
    """
    def __init__(self, *statements):
        for statement in statements:
            if not isinstance(statement, Statement):
                statement = Command(statement)
        self.statements = statements


class MainLogicJump(Statement):
    """
    Main logic jump is a statement used in the main logic of a unit to jump to another item.
    """
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


class _SwitchCase(object):
    def __init__(self, to_compare):
        self.to_compare = to_compare

    def __call__(self, *body_statements):
        self.body_statements = StatementCollection(body_statements)
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
    pass


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
        self.condition_commands = condition_commands
        self.condition_body = None
        self.otherwise_body = None

    def then(self, *statements):
        self.condition_body = Conditional(*statements)
        return self

    def otherwise(self, *statements):
        assert False, "otherwise is not implemented."
