"""Holds example unit"""
from cbac.unit.unit_base import Unit
from cbac.unit import std_logic, auto_synthesis


class ExampleUnit(Unit):
    """
    This is an example of a basic structure of a command block array unit.
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()
    @auto_synthesis
    def __init__(self, bits=8, inp=std_logic.InputRegister, output=std_logic.OutputRegister):
        super(ExampleUnit, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.my_input = self.add(inp)
        self.my_output = self.add(output)

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        yield self.my_input.shell.move(self.my_output)
