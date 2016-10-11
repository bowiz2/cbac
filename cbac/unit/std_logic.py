from cbac.block import Block
from cbac.constants.block_id import FALSE_BLOCK
from cbac.utils import memoize
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
    @memoize
    def blocks(self):
        """
        :return: List of blocks which compose the register.
        """
        return [In(self.default_block) for _ in xrange(self.size)]


class OutputRegister(Register):
    """
    Register which is an output.
    """

    @property
    @memoize
    def blocks(self):
        """
        :return: List of blocks which compose the register.
        """
        return [Out(self.default_block) for _ in xrange(self.size)]
