from sul.gate import Gate
from cbac.unit.statements import If
from cbac.unit import std_logic


class XnorGate(Gate):
    """
    Preform simple xor logic on 2 ports.
    """
    def __init__(self, a=std_logic.In, b=std_logic.In, s=std_logic.Out):
        super(XnorGate, self).__init__()
        self.a = self.add(a)
        self.b = self.add(b)
        self.s = self.add(s)

    def architecture(self):
        """
        Implement simple xor using a truth table.
        """

        yield If(
            (self.a.shell == False) & (self.b.shell == False)
        ).then(
            self.s.shell.activate()
        )
        yield If(
            (self.a.shell == True) & (self.b.shell == True)
        ).then(
            self.s.shell.activate()
        )

