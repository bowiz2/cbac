"""
Holds AND unit.
"""
from cbac.unit import Unit
from cbac.unit import std_logic
from cbac.unit.statements import If
from cbac.unit.vision import auto_synthesis


class AndUnit(Unit):
    @auto_synthesis
    def __init__(self, x=std_logic.In, y=std_logic.In, s=std_logic.Out):
        super(AndUnit, self).__init__()
        self.x = self.add(x)
        self.y = self.add(y)
        self.s = self.add(s)

    def architecture(self):
        yield If((self.x.shell == True) & (self.y.shell == True)).then(
            self.s.shell.activate()
        )