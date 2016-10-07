from cbac.unit import Unit
from cbac.unit.statements import If
from cbac.unit import std_logic, auto_synthesis
from sul.gate import Gate

class NotGate(Gate):
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

