from cbac.unit.unit_base import Unit
from cbac.unit.statements import If
from cbac.unit import std_logic, auto_synthesis
from sul.simple_array import Simple1pArray


class NotGate(Unit):
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


class NotGateArray(Simple1pArray):
    """
    Simple not gate array.
    """
    @auto_synthesis
    def __init__(self, bits, a=std_logic.InputRegister, s=std_logic.OutputRegister):
        super(NotGateArray, self).__init__(NotGate, bits, a, s)
