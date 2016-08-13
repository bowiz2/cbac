from command_shell import CompoundShell
from constants.block_id import FALSE_BLOCK


class MemoryShell(CompoundShell):
    def reset(self):
        """
        Set the memory to zero.
        """
        return self.fill(FALSE_BLOCK)
