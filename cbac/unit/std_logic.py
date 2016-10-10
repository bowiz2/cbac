from cbac.block import Block
from cbac.constants.block_id import FALSE_BLOCK
import cbac.compound.register
# TODO: fix the major bug.

class StdLogic(object):
    """
    Every std logic item is derived from this class.
    """
    pass


class Port(Block, StdLogic):
    """
    Represents a block.
    """

    def __init__(self):
        super(Port, self).__init__(FALSE_BLOCK)


class In(Port):
    """
    Ports which are used as input.
    """
    pass


class Out(Port):
    """
    Ports which are used as output.
    """
    pass


class Register(cbac.compound.register.Register, StdLogic):
    """
    Register inside the unit.
    soon all the registers must be of this type.
    """
    pass


class InputRegister(Register):
    """
    Register which is an input, used in a call statement.
    """
    @property
    def ports(self):
        for port in super(InputRegister, self).ports:



class OutputRegister(Register):
    """
    Register which is an output.
    """
    pass
