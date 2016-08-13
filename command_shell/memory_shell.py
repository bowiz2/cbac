from . import CompoundShell
from constants.block_id import FALSE_BLOCK, TRUE_BLOCK


class MemoryShell(CompoundShell):
    def reset(self):
        """
        Set the memory to zero.
        """
        return self.set_value(0)

    def set_value(self, number):
        """
        Sets the value of the memory, can be done to a limited set of numebrs
        """
        max = 2**self.wrapped.size
        possible_set = [0, max]
        if number == max:
            return self.fill(TRUE_BLOCK)
        if number == 0:
            return self.fill(FALSE_BLOCK)

    def set_max_value(self):
        """
        Sets the momeries value to the maximum possible value
        :return:
        """
        return self.set_value(2**self.wrapped.size)