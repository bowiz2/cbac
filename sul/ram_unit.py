from cbac.unit.unit_base import Unit
from cbac.compound import Register
from cbac.entity import Entity
from cbac.constants.entity_id import ARMOR_STAND
from cbac.unit.statements import Conditional
from cbac.constants.mc_direction import *
from cbac.blockbox import BlockBox
from cbac.constants.block_id import FALSE_BLOCK
from utils import Vector
import math
from sul.increment_unit import IncrementUnit
from cbac.unit.statements import STDCall


class RamUnit(Unit):
    def __init__(self, address_space_size=8, ratio=(1,16,16), word_size=8):
        """
        :param address_space_size: The size of the address space in bits.
        """
        self.ratio = Vector(*ratio)
        print self.ratio.x * self.ratio.y * self.ratio.z


        self.word_size = word_size
        self.address_space = address_space_size
        super(RamUnit, self).__init__(address_space_size)
        # == Here you declare all your memory slots.

        self.address_input = self.create_input(self.bits)
        self.read_output = self.create_output(self.bits)
        self.write_input = self.create_input(self.bits)
        blocksize = (self.ratio.x * 8, self.ratio.y, self.ratio.z)
        self.memory_box = self.add_compound(BlockBox(blocksize, FALSE_BLOCK))
        self.pivot = Entity(ARMOR_STAND, custom_name="RAM_PIVOT", no_gravity=True)
        # ==
        self.synthesis()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield self.pivot.shell.summon(self.memory_box[0][0][0])
        for i, addres_bit in enumerate(self.address_input.blocks):
            if 2**i < self.ratio.x:
                yield addres_bit.shell == True
                yield Conditional(
                    self.pivot.shell.move(EAST, self.word_size*(2 ** i))
                )
            elif 2**i < self.ratio.x + self.ratio.y-1:
                to_move = int(2 ** (i - math.log(self.ratio.x, 2)))
                yield addres_bit.shell == True
                yield Conditional(
                    self.pivot.shell.move(NORTH, to_move)
                )
            else:
                to_move = int(2 ** (i - math.log(self.ratio.x, 2) - math.log(self.ratio.y, 2)))
                yield addres_bit.shell == True
                yield Conditional(
                    self.pivot.shell.move(UP, to_move)
                )
        yield self.pivot.shell.activate()
        yield self.pivot.shell.kill()
