import math

from cbac.blockbox import BlockBox
from cbac.constants.block_id import FALSE_BLOCK
from cbac.constants.mc_direction import *
from cbac.unit.statements import *
from cbac.unit.unit_base import Unit
from cbac.utils import Vector, inline_generators
from cbac.entity.pivot import Pivot


class MemoryAccessUnit(Unit):
    """
    This unit provides basic functionality for accessing memory and preforming some user-defined action.

    See example of use in the ReadUnit.
    """

    def __init__(self, ratio=(1, 16, 16), word_size=8):
        """
        """
        ratio_product = 1
        for i in ratio:
            ratio_product *= i
        address_space_size = int(math.log(ratio_product, 2))

        super(MemoryAccessUnit, self).__init__(address_space_size)

        self.ratio = Vector(*ratio)
        self.word_size = word_size
        self.address_space = address_space_size

        self.address_input = self.create_input(self.bits)

        # The size of the box in which the memory is stored.
        memory_box_size = (self.ratio.x * self.word_size, self.ratio.y, self.ratio.z)
        self.memory_box = self.add_compound(BlockBox(memory_box_size, FALSE_BLOCK))

        # This pivot is going to move in the memory.
        # TODO: create pivot class with generated names.
        self.pivot = Pivot()
        # ==
        self.synthesis()

    @inline_generators
    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        # Reset the pivot.
        yield Debug("/say Resetting pivot.")
        yield self.pivot.shell.kill()
        # Create the pivot.
        yield self.pivot.shell.summon(self.memory_box[0][0][0])

        yield Debug("/say Moving pivot by address.")
        # Move it by to the address specified in the address register.
        for i, addres_bit in enumerate(self.address_input.blocks):
            if 2 ** i < self.ratio.x:
                yield If(
                    addres_bit.shell == True
                ).then(
                    self.pivot.shell.move(EAST, self.word_size * (2 ** i))
                )

            elif 2 ** i < self.ratio.x + self.ratio.y - 1:
                yield If(
                    addres_bit.shell == True
                ).then(
                    self.pivot.shell.move(NORTH, int(2 ** (i - math.log(self.ratio.x, 2))))
                )
            else:
                yield If(
                    addres_bit.shell == True
                ).then(
                    self.pivot.shell.move(UP, int(2 ** (i - math.log(self.ratio.x, 2) - math.log(self.ratio.y, 2))))
                )


class ReadUnit(Unit):
    def __init__(self, word_size, memory_access_unit):
        assert word_size == memory_access_unit.word_size, "read unit word-size must be equal to memory word size."
        super(ReadUnit, self).__init__(word_size)
        # Unit declaration.
        self.memory_access_unit = self.add_unit(memory_access_unit)

        self.address_input = self.add_input(self.memory_access_unit.address_input)
        self.read_output = self.create_output(self.word_size)
        self.synthesis()

    @property
    def word_size(self):
        return self.bits

    @property
    def pivot(self):
        return self.memory_access_unit.pivot

    def main_logic_commands(self):
        # We are not passing parameters because the inputs of the memory access unit are the same as this unit.
        yield InlineCall(self.memory_access_unit)
        yield self.pivot.shell.store_to_temp(self.read_output)
        yield self.read_output.shell.load_from_temp()
        yield Debug("?/say Read complete ok.")


class WriteUnit(Unit):
    def __init__(self, word_size, memory_access_unit):
        assert word_size == memory_access_unit.word_size, "read unit word-size must be equal to memory word size."
        super(WriteUnit, self).__init__(word_size)
        # Unit declaration.
        self.memory_access_unit = self.add_unit(memory_access_unit)

        self.address_input = self.add_input(self.memory_access_unit.address_input)
        self.data_input = self.create_input(self.word_size)
        self.synthesis()

    @property
    def word_size(self):
        return self.bits

    @property
    def pivot(self):
        return self.memory_access_unit.pivot

    def main_logic_commands(self):
        # We are not passing parameters because the inputs of the memory access unit are the same as this unit.
        yield InlineCall(self.memory_access_unit)
        yield self.data_input.shell.store_to_temp()
        yield self.pivot.shell.load_from_temp(self.data_input)
        yield Debug("?/say Write compete ok.")
