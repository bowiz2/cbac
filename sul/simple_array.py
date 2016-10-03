from cbac import Unit
from cbac.unit import std_logic
from cbac.unit.vision import auto_synthesis


class SimpleArray(Unit):
    """
    Maps a unit logic over a fixed number of ports.
    """
    @auto_synthesis
    def __init__(self, logic, bits, x=std_logic.InputRegister, y=std_logic.InputRegister, s=std_logic.OutputRegister):
        super(SimpleArray, self).__init__(bits)
        self.x = self.add(x)
        self.y = self.add(y)
        self.s = self.add(s)
        self.logic = self.add(logic)

    def architecture(self):
         yield map(self.logic, self.x.ports, self.y.ports, self.s.ports)