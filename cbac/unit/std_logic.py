from cbac.block import Block
from cbac.constants.block_id import FALSE_BLOCK
from cbac.compound.register import Register

class StdLogic(object):
    pass

class Port(Block,StdLogic):
    def __init__(self):
        super(Port, self).__init__(FALSE_BLOCK)


class In(Port):
    pass


class Out(Port):
    pass


class IORegister(Register, StdLogic):
    pass


class InputRegister(IORegister):
    pass


class OutputRegister(IORegister):
    pass