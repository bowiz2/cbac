from cbac.unit import Unit
from cbac.unit import std_logic
from cbac.unit.statements import *

# This is the vision for MHDL


class AND(Unit):
    def __init__(self, x=std_logic.In, y=std_logic.In, s=std_logic.Out):
        super(AND, self).__init__()
        self.x = self.add(x)
        self.y = self.add(y)
        self.s = self.add(s)

    def architecture(self):
        yield If(self.x.shell == self.y).then(self.s.shell.activate())

class AndXBit(Unit):

    def __init__(self, bit, x=std_logic.InputRegister, y=std_logic.InputRegister, z=std_logic.OutputRegister, logic=AND):
        super(AndXBit, self).__init__(bit)
        self.x = self.add_input(x)
        self.y = self.add_input(y)
        self.s = self.add_output(z)
        self.logic = logic

    def architecture(self):
         yield map(self.logic, zip(self.x.ports, self.y.ports, self.s.ports))

