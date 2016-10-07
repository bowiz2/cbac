from cbac import Unit
from unit import auto_synthesis, std_logic
from unit.statements import If


class NandGate(Unit):
    """
    Simple NAND logic.
    """
    @auto_synthesis
    def __init__(self, a=std_logic.In, b=std_logic.In, s=std_logic.Out):
        super(NandGate, self).__init__()
        self.a = self.add(a)
        self.b = self.add(b)
        self.s = self.add(s)

    def architecture(self):
        yield self.s.shell.activate()
        yield If((self.a.shell == True) & (self.shell == True)).then(self.s.shell.deactivate())