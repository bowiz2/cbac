from cbac import Unit
from cbac.unit import std_logic
from cbac.unit.vision import auto_synthesis


class SimpleArray(Unit):
    """
    Maps a unit logic over a fixed number of ports.
    """

    @auto_synthesis
    def __init__(self, bits, gate, *interfaces):
        """
        :param gate: the gate of which the array is of .
        :param bits: default size of the registers in this array.
        :param registers: list of input registers and the last register is an output register.
        """
        super(SimpleArray, self).__init__(bits)
        self.interfaces = [self.add(interface) for interface in interfaces]
        self.gate = self.add(gate)

    def architecture(self):
        yield map(self.gate, *[interface.ports for interface in self.interfaces])
