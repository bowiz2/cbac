"""Holds example unit"""
from cbac.unit.unit_base import Unit


class ExampleUnit(Unit):
    """
    This is an example of a basic structure of a command block array unit.
    """

    def __init__(self, bits=8):
        super(ExampleUnit, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.my_input = self.create_input(self.bits)
        self.my_output = self.create_output(self.bits)
        # ==
        # Dont forget to synthesises your nodule.
        self.synthesis()

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        yield self.my_input.shell.move(self.my_output)
