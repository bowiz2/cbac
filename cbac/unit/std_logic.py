from cbac.block import Block
from cbac.constants.block_id import FALSE_BLOCK
import cbac.compound.register

class StdLogic(object):
    pass

class Port(Block,StdLogic):
    def __init__(self):
        super(Port, self).__init__(FALSE_BLOCK)


class In(Port):
    pass


class Out(Port):
    pass


class Register(cbac.compound.register.Register, StdLogic):
    pass


class InputRegister(Register):
    pass


class OutputRegister(Register):
    pass