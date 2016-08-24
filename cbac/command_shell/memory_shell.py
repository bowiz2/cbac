from cbac.constants.block_id import TRUE_BLOCK
from . import CompoundShell


class RegisterShell(CompoundShell):
    def reset(self):
        """
        Set the memory to zero.
        """
        return self.set_value(0)

    def set_value(self, number):
        """
        Sets the value of the memory, can be done to a limited set of numebrs
        """
        max = 2 ** self.wrapped.size
        possible_set = [0, max]
        if number == max:
            return self.fill(TRUE_BLOCK)
        if number == 0:
            return self.fill(self.wrapped.default_block)

    def set_max_value(self):
        """
        Sets the momeries value to the maximum possible value
        :return:
        """
        return self.set_value(2 ** self.wrapped.size)