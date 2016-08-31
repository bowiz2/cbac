"""
Statements are syntactic sugar for the definition of units.
"""
# TODO: implement switch statement.


class Statement(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped


class MainLogicJump(Statement):
    """
    Main logic jump is a statement used in the main logic of a unit to jump to another item.
    """
    pass


class Conditional(Statement):
    def __init__(self, *commands):
        super(Conditional, self).__init__(commands)

    @property
    def commands(self):
        return self.wrapped

class PassParameters(Statement):
    def __init__(self, unit, *parameters):
        super(PassParameters, self).__init__(unit)
        self.parameters = parameters


class Call(Statement):
    @property
    def called_unit(self):
        return self.wrapped


class STDCall(Call, PassParameters, MainLogicJump):
    pass


class StatementOption(object):
    pass


class SwitchCase(StatementOption):
    def __init__(self, wrap):
        self.wrap = wrap
    def __call__(self, *to_do):
        self.to_do = to_do

class _SwitchCaseSugar(StatementOption):
    """
    Singleton
    """
    def __getitem__(self, item):
        return SwitchCase(item)

class InlineCall(Call, PassParameters):
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
       