from cbac.unit.unit_base import Unit
from cbac.unit.statements import If
from cbac.unit.vision import auto_synthesis
from cbac.unit import std_logic


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


class NandArray(Unit):
    """
    Array of nand gates
    """
    @auto_synthesis
    def __init__(self, bits=8, a=std_logic.InputRegister, b=std_logic.InputRegister, s=std_logic.OutputRegister):
        super(NandArray, self).__init__(bits)
        self.a = self.add(a)
        self.b = self.add(b)
        self.s = self.add(s)

    def architecture(self):
        yield self.s.shell.set_max_value()
        for a_port, b_port, s_port, in zip(self.a.ports, self.b.ports, self.s.ports):
            yield If((a_port.shell == True) & (b_port.shell == True)).then(s_port.shell.deactivate())

