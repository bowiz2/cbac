from cbac.unit import Unit
from cbac.unit import std_logic
from cbac.unit.statements import *

def auto_synthesis(f):
    # TODO: write tests for this
    def wrapper(u_self, *args, **kwargs):
        do_synthesise = True
        if "auto_synthesis" in kwargs.keys():
            do_synthesise = kwargs.pop("auto_synthesis")

        f(u_self, *args, **kwargs)
        if do_synthesise:
            u_self.synthesis()

    wrapper.__name__ = f.__name__
    return wrapper


# This is the vision for MHDL

class AND(Unit):
    @auto_synthesis
    def __init__(self, x=std_logic.In, y=std_logic.In, s=std_logic.Out):
        super(AND, self).__init__()
        self.x = self.add(x)
        self.y = self.add(y)
        self.s = self.add(s)
        #self.synthesis()

    def architecture(self):
        yield If((self.x.shell == True) & (self.y.shell == True)).then(
            self.s.shell.activate()
        )


class LogicArray(Unit):
    @auto_synthesis
    def __init__(self, bit, x=std_logic.InputRegister, y=std_logic.InputRegister, z=std_logic.OutputRegister, logic=AND):
        super(LogicArray, self).__init__(bit)
        self.x = self.add(x)
        self.y = self.add(y)
        self.s = self.add(z)
        self.logic = self.add(logic)

    def architecture(self):
         yield map(self.logic, self.x.ports, self.y.ports, self.s.ports)
