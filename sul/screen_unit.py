from cbac.unit.unit_base import Unit
from pymclevel import MCSchematic
from cbac.unit.statements import *
from sul import MemoryAccessUnit
import math
# TODO: explain what is a char set schematic
# TODO: support vertical screens.


class ScreenUnit(Unit):
    def __init__(self, char_set, memory_access_unit):
        """
        :param char_set: Path to a char-set schematic
        :param memory_access_unit: we treat the screen as a memory.
        """
        super(ScreenUnit, self).__init__(0)
        char_set = MCSchematic(char_set)

        self.char_set = self.add_compound(char_set)
        # How many different characters this screen can printout.
        self.char_set_size = char_set.size[1]
        # 2 dimensional area which is taken by a character.
        self.character_sprite_area = (char_set.size[0], char_set.size[2])

        self.char_set_access_unit = self.add_unit(MemoryAccessUnit())
        self.screen_access_unit = self.add_unit(memory_access_unit)
        self.location_input = self.add_input(self.screen_access_unit.address_input)
        # TODO: think of a better name.
        # What is the order over the char you want to print
        self.print_value_input = self.create_input(self.bits)

        self.synthesis()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield InlineCall(self.screen_access_unit)

