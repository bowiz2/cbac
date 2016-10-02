from cbac.unit.unit_base import Unit
from pymclevel import MCSchematic
from cbac.unit.statements import *
from sul import MemoryAccessUnit
# TODO: explain what is a char set schematic
# TODO: support vertical screens.


class ScreenUnit(Unit):
    def __init__(self, char_set, screen_access_unit):
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

        # This is the unit which will give us the way to navigate in the charecters.
        self.char_set_access_unit = self.add_unit(
            MemoryAccessUnit((1, self.char_set_size, 1), self.character_sprite_area)
        )
        self.print_value_input = self.add_input(self.char_set_access_unit.address_input)
        self.screen_access_unit = self.add_unit(screen_access_unit)
        self.location_input = self.add_input(self.screen_access_unit.address_input)
        # TODO: think of a better name.
        # What is the order over the char you want to print
        self.synthesis()

    def main_logic_commands(self):
        yield InlineCall(self.char_set_access_unit)
        yield InlineCall(self.screen_access_unit)
        yield self.char_set_access_unit.pivot.shell.store_to_temp(self.character_sprite_area)
        yield self.screen_access_unit.pivot.shell.load_from_temp(self.character_sprite_area)
