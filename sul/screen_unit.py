from cbac.unit.unit_base import Unit
from pymclevel import MCSchematic
from cbac.unit.statements import *
from sul import MemoryAccessUnit
from cbac.utils import Vector
from cbac.unit import auto_synthesis

# TODO: explain what is a char set schematic
# TODO: support vertical screens.


class ScreenUnit(Unit):
    """
    Implements a screen in minecraft.
    This unit has two registers:
        - character input: indicates which character in the char set will be printed
        - position input: indicates the location on the screen at which the character will be printed.
    """
    @auto_synthesis
    def __init__(self, char_set, screen_access_unit):
        """
        :param char_set: Path to a char-set schematic
        :param memory_access_unit: we treat the screen as a memory.
        """
        super(ScreenUnit, self).__init__(0)

        if not isinstance(char_set, MCSchematic):
            char_set = MCSchematic(filename=char_set)

        self.char_set = self.add_compound(char_set)
        # How many different characters this screen can printout.
        self.char_set_size = int(char_set.size[1])
        # 2 dimensional area which is taken by a character.
        self.character_sprite_size = (int(char_set.size[0]), 1, int(char_set.size[2]))

        # This is the unit which will give us the way to navigate in the charecters.
        self.char_set_access_unit = self.add_unit(
            MemoryAccessUnit((1, self.char_set_size, 1), self.character_sprite_size, self.char_set)
        )
        assert self.char_set_access_unit.word_size == screen_access_unit.word_size, \
            "char set word size must equal to the screen."
        self.screen_access_unit = self.add_unit(screen_access_unit)

        self.input_character = self.add_input(self.char_set_access_unit.input_address)
        self.input_location = self.add_input(self.screen_access_unit.input_address)



    def architecture(self):
        yield InlineCall(self.char_set_access_unit)
        yield InlineCall(self.screen_access_unit)
        yield self.char_set_access_unit.pivot.shell.store_to_temp(
            ((0, 0, 0), Vector(*self.character_sprite_size) - Vector(1, 1, 1)))
        yield self.screen_access_unit.pivot.shell.load_from_temp(
            ((0, 0, 0), Vector(*self.character_sprite_size) - Vector(1, 1, 1)))
