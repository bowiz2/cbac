"""
Holds all memory access and manipulation units.
"""
import math

from cbac.core.blockbox import BlockBox, PlainBlockBox
from core.block import BlockID
from cbac.core.mc_direction import MCDirection
from cbac.core.mcentity.pivot import Pivot
from cbac.core.utils import Vector, inline_generators
from cbac.unit.statements import *
from cbac.unit.unit_base import Unit
from cbac import std_logic
from cbac.core.compound.hardware_constant import HardwareConstant
from cbac.core.utils import memoize


class MemoryDump(BlockBox):
    """
    Represents raw memory.
    """

    def __init__(self, data, ratio=(1, 16, 16), word_length=8, isolated=False):
        super(MemoryDump, self).__init__((word_length * ratio[0], ratio[1], ratio[2]), isolated)
        self.ratio = ratio
        assert len(data) <= self.max_data_size
        self.word_length = word_length
        self.data = data
        self.complete_data()

    @property
    def max_data_size(self):
        """
        Calculate the maximum size of the data.
        """
        return self.ratio[0] * self.ratio[1] * self.ratio[2]

    def complete_data(self):
        """
        Fills the data array so it will match the whole memory.
        :return:
        """
        while len(self.data) < self.max_data_size:
            self.data.append(0)

    @property
    @memoize
    def blocks(self):
        constants = [HardwareConstant(i, word_size=self.word_length).blocks for i in self.data]
        rows = self.group(constants, self.ratio[1])
        return rows

    def group(self, items, group_size):
        import copy
        groups = []
        cur_group = []
        items = copy.copy(items)
        while len(items) > 0:
            for _ in xrange(group_size):
                cur_group.append(items.pop(0))
            groups.append(cur_group)
            cur_group = []

        return groups


class MemoryAccessUnit(Unit):
    """
    This unit provides basic functionality for accessing memory and preforming some user-defined action.

    See example of use in the ReadUnit.
    """

    def __init__(self, ratio=(1, 16, 16), word_size=(8, 1, 1), memory_dump=None, input_address=std_logic.InputRegister):
        """
        :param ratio: The ration of words distributed in 3D space.
        :param word_size: the size of a word. by default it is a 8 bits facing east.
        :param memory_dump: This is the actual "raw" memory on which this access unit is operating.
        If no is specified, Memory block will be generated from the ratios multiplied by the word size.
        """
        ratio_product = 1
        for i in ratio:
            ratio_product *= i
        address_space_size = int(math.log(ratio_product, 2))
        word_size = Vector(*word_size)

        super(MemoryAccessUnit, self).__init__(address_space_size)
        # The address you want to access
        self.input_address = self.add_input(input_address)

        self.ratio = Vector(*ratio)
        self.word_size = word_size
        self.address_space = address_space_size

        if not memory_dump:
            # The size of the box in which the memory is stored.
            memory_box_size = (
                self.ratio.x * self.word_size.x,
                self.ratio.y * self.word_size.y,
                self.ratio.z * self.word_size.z
            )
            memory_dump = PlainBlockBox(memory_box_size, BlockID.FALSE_BLOCK)

        # raw memory is the actual blocks which represent the memory.
        self.raw_memory = self.add_compound(memory_dump)

        # This pivot is going to move in the memory.
        self.pivot = Pivot()
        # ==
        self.synthesis()

    @inline_generators
    def architecture(self):
        """
        Describe hardware behavior
        """
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        # Reset the pivot.
        # TODO: document
        yield self.pivot.shell.kill()
        # Create a new pivot.
        yield self.pivot.shell.summon(self.raw_memory)

        # Move it by to the address specified in the address register.
        for i, addres_bit in enumerate(self.input_address.blocks):
            if 2 ** i < self.ratio.x:
                yield If(addres_bit.shell == True).then(
                    self.pivot.shell.move(MCDirection.EAST, self.word_size.x * (2 ** i))
                )

            elif 2 ** i < self.ratio.x + self.ratio.y - 1:
                yield If(addres_bit.shell == True).then(
                    self.pivot.shell.move(MCDirection.UP, self.word_size.y * int(2 ** (i - math.log(self.ratio.x, 2)))
                                          )
                )
            else:
                yield If(addres_bit.shell == True).then(
                    self.pivot.shell.move(
                        MCDirection.NORTH,
                        self.word_size.z * int(2 ** (i - math.log(self.ratio.x, 2) - math.log(self.ratio.y, 2)))
                    )
                )


class ReadUnit(Unit):
    """
    Reads data from memory.
    """

    def __init__(self, word_size, memory_access_unit, read_output=std_logic.OutputRegister):
        """
        :param word_size: The size of the words this unit can read. (8 bits for example)
        :param memory_access_unit: Unit which can access memory.
        :param read_output: Register to which the read data will be saved.
        """
        assert (word_size, 1,
                1) == memory_access_unit.word_size, "read unit word-size must be equal to memory word size."
        super(ReadUnit, self).__init__(word_size)
        # Unit declaration.
        self.memory_access_unit = self.add_unit(memory_access_unit)

        self.address_input = self.add_input(self.memory_access_unit.input_address)
        self.read_output = self.add_output(read_output)
        self.synthesis()

    @property
    def word_size(self):
        """
        The size of the words this unit can read. (8 bits for example)
        """
        return self.bits

    @property
    def pivot(self):
        """
        :return: Pivot instance which preforms the read operation.
        """
        return self.memory_access_unit.pivot

    def architecture(self):
        """
        Describe hardware behavior
        """
        # We are not passing parameters because the inputs of the memory access unit are the same as this unit.
        yield InlineCall(self.memory_access_unit)
        yield self.pivot.shell.store_to_temp(self.read_output)
        yield self.read_output.shell.load_from_temp()


class WriteUnit(Unit):
    """
    Writes data to memory
    """

    def __init__(self, word_size, memory_access_unit, data_input=std_logic.InputRegister):
        """
        :param word_size: What is the size of the data this unit can write
        :param memory_access_unit: Unit which can access memory.
        :param data_input: Register from which the data will be take for writing.
        """
        assert (word_size, 1,
                1) == memory_access_unit.word_size, "read unit word-size must be equal to memory word size."
        super(WriteUnit, self).__init__(word_size)
        # Unit declaration.
        self.memory_access_unit = self.add_unit(memory_access_unit)

        self.address_input = self.add_input(self.memory_access_unit.input_address)
        self.data_input = self.add_input(data_input)
        self.synthesis()

    @property
    def word_size(self):
        """
        What is the size of the data this unit can write
        """
        return self.bits

    @property
    def pivot(self):
        """
        :return: Pivot instance which preforms the write operation.
        """
        return self.memory_access_unit.pivot

    def architecture(self):
        """
        Describe hardware behavior
        """
        # We are not passing parameters because the inputs of the memory access unit are the same as this unit.
        yield InlineCall(self.memory_access_unit)
        yield self.data_input.shell.store_to_temp()
        yield self.pivot.shell.load_from_temp(self.data_input)
