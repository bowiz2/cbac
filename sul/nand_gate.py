from cbac import std_logic
from cbac import std_unit
from sul.nand_array import NandArray
from unit import auto_synthesis
from unit.statements import If


class NandGate(std_unit.Gate):
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

    @classmethod
    def Array(cls, size=None):
        """
        Get an array of nand gates.
        """
        array_class = NandArray
        if size:
            return array_class(size)
        return array_class
