from cbac.unit.unit_base import Unit
from cbac.compound import Register
from cbac.entity import Entity
from cbac.constants.entity_id import ARMOR_STAND
from cbac.unit.statements import Conditional
from cbac.constants.mc_direction import *


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
        self.pivot_home = self.add_compound(Register(1))
        self.pivot = Entity(ARMOR_STAND, custom_name="RAM_PIVOT", no_gravity=True)
        # ==
        self.synthesis()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield self.pivot.shell.summon(self.pivot_home)
        for i, addres_bit in enumerate(self.address_input.blocks):
            yield addres_bit.shell == True
            yield Conditional(
                self.pivot.shell.move(UP, 2 ** i)
            )
        yield self.pivot.shell.activate()
        yield self.pivot.shell.kill()
