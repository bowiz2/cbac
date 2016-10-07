from cbac.unit.unit_base import Unit
from cbac.unit.statements import *
from cbac.unit.vision import auto_synthesis
from cbac.unit import std_logic


class FullAdderUnit(Unit):
    """
    Preform
    """
    @auto_synthesis
    def __init__(self, a=std_logic.In, b=std_logic.In, s=std_logic.Out, cin=std_logic.In, cout=std_logic.Out):
        super(FullAdderUnit, self).__init__()
        self.a = self.add(a)
        self.b = self.add(b)
        self.s = self.add(s)
        self.cin = self.add(cin)
        self.cout = self.add(cout)

    def architecture(self):
        """
        Simple full adder architecture using a truth table.
        """
        # TODO: create a truth table statement.
        yield self.a.shell == False
        yield self.b.shell == False
        yield self.cin.shell == True
        yield Conditional(
            self.s.shell.activate()
        )
        yield self.a.shell == False
        yield self.b.shell == True
        yield self.cin.shell == False
        yield Conditional(
            self.s.shell.activate()
        )
        yield self.a.shell == False
        yield self.b.shell == True
        yield self.cin.shell == True
        yield Conditional(
            self.cout.shell.activate()
        )
        yield self.a.shell == True
        yield self.b.shell == False
        yield self.cin.shell == False
        yield Conditional(
            self.s.shell.activate()
        )
        yield self.a.shell == True
        yield self.b.shell == False
        yield self.cin.shell == True
        yield Conditional(
            self.cout.shell.activate()
        )
        yield self.a.shell == True
        yield self.b.shell == True
        yield self.cin.shell == False
        yield Conditional(
            self.cout.shell.activate()
        )
        yield self.a.shell == True
        yield self.b.shell == True
        yield self.cin.shell == True
        yield Conditional(
            self.cout.shell.activate(),
            self.s.shell.activate()
        )

    @classmethod
    def Array(cls, size=None):
        """
        Get the array of full adder.
        :param size:
        :return:
        """
        array = RippleCarryFullAdderArray
        if size:
            return array(size)
        return array


class RippleCarryFullAdderArray(Unit):
    """
    Implement an array of full adders, resulting in a calculator.
    """
    @auto_synthesis
    def __init__(self, bits, input_a=std_logic.InputRegister, input_b=std_logic.InputRegister,
                 output=std_logic.OutputRegister, full_adder_logic=FullAdderUnit, carry_flag=None):
        super(RippleCarryFullAdderArray, self).__init__(bits)
        self.input_a = self.add(input_a)
        self.input_b = self.add(input_b)
        self.output = self.add(output)
        self.carry = self.add(std_logic.InputRegister(self.bits+1))
        self.carry_flag = self.add(carry_flag)
        self.full_adder_logic = self.add(full_adder_logic)

    def architecture(self):
        """
        Simple implementation of a full adder array.
        """
        yield map(self.full_adder_logic, self.input_a.ports, self.input_b.ports, self.output.ports,
                  self.carry.ports[:-1], self.carry.ports[1:])
        if self.carry_flag:
            self.carry.ports[-1].shell.copy(self.carry_flag)
