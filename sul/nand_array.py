from cbac.unit import std_logic
from cbac.unit.statements import If
from cbac.unit.unit_base import Unit
from cbac.unit.vision import auto_synthesis


class NandArray(Unit):
    """
    Array of nand gates
    """

    @auto_synthesis
    def __init__(self, bits=8, a=std_logic.InputRegister, b=std_logic.InputRegister, s=std_logic.OutputRegister):
        super(NandArray, self).__init__(bits)
        self.input_a = self.add_input(a)
        self.input_b = self.add_input(b)
        self.output = self.add_output(s)

    def architecture(self):
        yield self.output.shell.set_max_value()
        for a_port, b_port, s_port, in zip(self.input_a.ports, self.input_b.ports, self.output.ports):
            yield If((a_port.shell == True) & (b_port.shell == True)).then(s_port.shell.deactivate())
