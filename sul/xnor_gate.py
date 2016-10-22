from cbac.unit.statements import If
from std_logic import io
from std_unit.gate import Gate


class XnorGate(Gate):
    """
    Preform simple xor logic on 2 ports.
    """

    def __init__(self, a=io.In, b=io.In, s=io.Out):
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
