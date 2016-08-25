"""
Statements are syntactic sugar for the definition of units.
"""


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


class STDCall(Statement):
    def __init__(self, called_unit, *parameters):
        self.called_unit = called_unit
        self.parameters = parameters


class If(Statement):
    def __init__(self, condition_command):
        super(If, self).__init__([])
        self.condition_command = condition_command
        self.condition_body = None
        self.otherwise_body = None

    def then(self, *statements):
        self.condition_body = Conditional(*statements)
        return self

    def otherwise(self, *statements):
        assert False, "otherwise is not implemented."
        # self.otherwise_body = statements
