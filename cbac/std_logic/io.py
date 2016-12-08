"""
Holds the io sugar.
"""
from core.block import BlockID

import cbac.core.compound.register
import cbac.core.block


class StdLogic(object):
    """
    Every std logic item is derived from this class.
    """
    pass


class Port(cbac.core.block.Block, StdLogic):
    """
    Represents a block.
    """

    def __init__(self, fill_block_id=BlockID.FALSE_BLOCK):
        super(Port, self).__init__(fill_block_id)


class In(Port):
    """
    Semantic class for object generation
    """
    pass


class Out(Port):
    """
    Semantic class for object generation
    """
    pass


class Register(cbac.core.compound.register.Register, StdLogic):
    """
    Register inside the unit.
    soon all the registers must be of this type.
    """
    pass


class InputRegister(Register):
    """
    Semantic class for object generation
    """
    pass


class OutputRegister(Register):
    """
    Semantic class for object generation
    """
    pass
