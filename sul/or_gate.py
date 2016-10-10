from cbac.unit.statements import If
from sul.gate import Gate
from cbac.unit import std_logic, auto_synthesis


class OrGate(Gate):
    """
    Simple Bitwise Or Gate
    """

    @auto_synthesis
    def __init__(self, a=std_logic.In, b=std_logic.In, s=std_logic.Out):
        super(OrGate, self).__init__()
        self.a = self.add(a)
        self.b = self.add(b)
        self.s = self.add(s)

    def architecture(self):
        yield If(self.a.shell == True).then(self.s.shell.activate())
        yield If(self.b.shell == True).then(self.s.shell.activate())
