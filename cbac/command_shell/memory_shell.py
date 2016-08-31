"""
Holds register shell.
"""
from cbac.constants.block_id import TRUE_BLOCK

from . import CompoundShell


class RegisterShell(CompoundShell):
    """
    Wraps the register object and provides command interface for it.
    """
    def reset(self):
        """
        Set the memory to zero.
        """
        return self.set_value(0)

    def set_value(self, number):
        """
        Sets the value of the memory, can be done to a limited set of numebrs
        """

        # TODO: work on the set value feature.
        max_value = 2 ** self.wrapped.size

        if number == max_value:
            return self.fill(TRUE_BLOCK)
        if number == 0:
            return self.fill(self.wrapped.default_block)

    def set_max_value(self):
        """
        Sets the momeries value to the maximum possible value
        :return:
        """
        return self.set_value(2 ** self.wrapped.size)
