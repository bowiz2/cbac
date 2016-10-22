"""
Holds AND unit.
"""
from cbac.unit.decorators import auto_synthesis
from cbac.unit.statements import If
from cbac import std_logic


class AndGate(std_logic.Gate):
    """
    Simple bitwise and logic on two ports.
    """

    @auto_synthesis
    def __init__(self, a=std_logic.In, b=std_logic.In, s=std_logic.Out):
        super(AndGate, self).__init__()
        self.a = self.add(a)
        self.b = self.add(b)
        self.s = self.add(s)

    def architecture(self):
        yield If((self.a.shell == True) & (self.b.shell == True)).then(
            self.s.shell.activate()
        )
