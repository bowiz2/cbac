from cbac import Unit
from unit import std_logic
from unit.vision import auto_synthesis
from and_unit import AndUnit


class SimpleArray(Unit):
    @auto_synthesis
    def __init__(self, bit, x=std_logic.InputRegister, y=std_logic.InputRegister, z=std_logic.OutputRegister, logic=AndUnit):
        super(SimpleArray, self).__init__(bit)
        self.x = self.add(x)
        self.y = self.add(y)
        self.s = self.add(z)
        self.logic = self.add(logic)

    def architecture(self):
         yield map(self.logic, self.x.ports, self.y.ports, self.s.ports)