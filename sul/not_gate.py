from cbac.unit import auto_synthesis
from cbac.unit.statements import If
from cbac import std_logic
from cbac import std_unit


class NotGate(std_unit.Gate):
    """
    Simple not gate implementation.
    """

    @auto_synthesis
    def __init__(self, a=std_logic.In, s=std_logic.Out):
        super(NotGate, self).__init__()
        self.a = self.add(a)
        self.s = self.add(s)

    def architecture(self):
        yield If(self.a.shell == False).then(self.s.shell.activate())
        yield If(self.a.shell == True).then(self.s.shell.deactivate())
