from unit import Unit
from compound import Memory
from entity import Entity
from constants.entity_id import ARMOR_STAND
from unit import Conditional
from constants.direction import *


class RamUnit(Unit):
    def __init__(self, address_space):
        """
        :param address_space: The size of the address space in bits.
        """
        self.address_space = address_space
        super(RamUnit, self).__init__(address_space)
        # == Here you declare all your memory slots.
        self.address_input = self.create_input(self.bits)
        self.read_output = self.create_output(self.bits)
        self.write_input = self.create_input(self.bits)
        self.pivot_home = self.add_compound(Memory(1))
        self.pivot = Entity(ARMOR_STAND, custom_name="RAM_PIVOT", no_gravity=True)
        # ==
        self.generate_main_logic_cbas()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield self.pivot.shell.summon(self.pivot_home)
        for i, addres_bit in enumerate(self.address_input.blocks):
            yield addres_bit.shell == True
            yield Conditional(
                self.pivot.shell.move(UP, 2**i)
            )
        yield self.pivot.shell.activate()
        yield self.pivot.shell.kill()