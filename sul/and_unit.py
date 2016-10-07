"""
Holds AND unit.
"""
from cbac.unit import Unit
from cbac.unit import std_logic
from cbac.unit.statements import If
from cbac.unit.vision import auto_synthesis


class AndGate(Unit):
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