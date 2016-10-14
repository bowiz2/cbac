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

    def __init__(self, fill_block_id=FALSE_BLOCK):
        super(Port, self).__init__(fill_block_id)

In = Port
Out = Port


class Register(cbac.compound.register.Register, StdLogic):
    """
    Register inside the unit.
    soon all the registers must be of this type.
    """
    pass


InputRegister = Register
OutputRegister = Register
