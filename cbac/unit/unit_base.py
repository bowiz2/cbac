from cbac.unit.logic_parser import UnitLogicParser
import itertools
from cbac.command_shell import UnitShell
from cbac.compound import Register
from cbac.utils import memoize


class Unit(object):
    def __init__(self, bits=None, logic_parser_instance=None):
        """
        Create a unit with an input base length.
        :param bits: The base length of the unit.
        """
        if not logic_parser_instance:
            logic_parser_instance = UnitLogicParser()
        self.bits = bits
        self._logic_parser = logic_parser_instance
        self.compounds = []
        self.inputs = []
        self.outputs = []
        # Units which are needed for this unit to function.
        self.dependent_units = []
        # Logic cbas are cbac which excecute the logic of the unit. the entry point is the first logic_cba
        self.logic_cbas = []
        self.is_inline = False

    def synthesis(self):
        """
        Takes the entry commands main logic commands and exit commands, and compiles them into a collection of CBAs.
        This collection is called logic_cbac.
        :return: None
        """

        logic_cbas, other_compounds = self._logic_parser.parse(
            itertools.chain(self.on_entry_init_commands(), self.main_logic_commands(), self.on_exit_commands())
        )
        # Add the CBAs to the unit.
        for parsed_item in logic_cbas + other_compounds:
            self.add_compound(parsed_item)

        self.logic_cbas = logic_cbas

    def add_compound(self, compound):
        """
        Add a compound to the compound list, meaning it will be compiled with the unit.
        :return: the added compound.
        """
        self.compounds.append(compound)
        return compound

    def add_unit(self, unit):
        """
        Adds a unit to the dependent unit list.
        :return: The added unit.
        """
        self.dependent_units.append(unit)
        return unit

    def add_input(self, register):
        """
        Set a register as an input for this unit. And return it.
        """
        self.inputs.append(register)
        self.add_compound(register)
        return register

    def add_output(self, register):
        """
        Sets a register as an output of this unit. And return it.
        """
        self.outputs.append(register)
        self.add_compound(register)
        return register

    def create_input(self, bits):
        """
        Creates a memory compound, adds it to the "inputs" list and returns it.
        """
        inp = Register(size=bits)
        return self.add_input(inp)

    def create_output(self, bits):
        """
        Creates a memory compound, adds it to the "inputs" list and returns it.
        """
        output = Register(size=bits)
        return self.add_output(output)

    def on_entry_init_commands(self):
        """
        Generate the commands which are executed when the entry pointed activated.
        """
        for output_memory in self.outputs:
            yield output_memory.shell.reset()

    def main_logic_commands(self):
        """
        Generates the main logic of the entry point cba.
        """
        pass

    def on_exit_commands(self):
        """
        Generate the commands which will be called when the main activation of the entry point is finished.
        :return:
        """
        for input_memory in self.inputs:
            yield input_memory.shell.reset()

    @property
    def compounds_to_pack(self):
        if self.is_inline:
            return filter(lambda compound: compound not in self.logic_cbas, self.compounds)
        else:
            return self.compounds

    @property
    def entry_point(self):
        """
        The first cba which needs to be activated in-order of the unit to preform its task.
        :return: CBA
        """
        return self.logic_cbas[0]

    @property
    def activator(self):
        """
        Returns the block which needs to be set to TRUE BLOCK in-order for the unit to fire-up.
        :return: Block
        """
        return self.logic_cbas[0].blocks[0]

    @property
    @memoize
    def shell(self):
        return UnitShell(self)
