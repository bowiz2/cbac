from cbac.unit.logic_parser import UnitLogicParser
import itertools
from cbac.command_shell import UnitShell
from cbac.compound import Register
from cbac.utils import memoize
from cbac.unit import std_logic
from cbac.block import Block
from cbac.constants.block_id import FALSE_BLOCK


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

        logic_cbas, other_compounds, other_units = self._logic_parser.parse(
            itertools.chain(self.on_entry_init_commands(), self.architecture(), self.on_exit_commands())
        )
        # Add the CBAs to the unit.
        for parsed_item in logic_cbas + other_compounds:
            self.add(parsed_item)
        for other_unit in other_units:
            self.add_unit(other_unit)
        self.logic_cbas = logic_cbas

    def add(self, item):
        """
        Add a compound to the compound list, meaning it will be compiled with the unit.
        :return: the added compound.
        """
        if isinstance(item, std_logic.StdLogic):
            if isinstance(item, std_logic.IORegister):
                item = Register(self.bits)
            if isinstance(item, std_logic.Port):
                item = Block(FALSE_BLOCK)
        self.compounds.append(item)
        return item

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
        register = self.add(register)
        self.inputs.append(register)
        return register

    def add_output(self, register):
        """
        Sets a register as an output of this unit. And return it.
        """
        register = self.add(register)
        self.outputs.append(register)
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
        if len(self.logic_cbas) < 1:
            raise Exception("This unit has not entry point.")
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

    def entity(self):
        """
        Entity is the description of the interface between a design and its external environment.
        It may also specify the declarations and statements that are part of the design entity.
        A given entity declaration may be shared by many design entities, each of which has a different architecture.
        Thus, an entity declaration can potentially represent a class of design entities, each having the same interface.
        """
        pass

    def architecture(self):
        """
        A body associated with an entity declaration to describe the internal organization or operation of a design entity.
        An architecture body is used to describe the behavior, data flow, or structure of a design entity.
        """
        pass


class SimpleUnit(Unit):
    """
    A simple unit has no input/output registers. it only preforms logic.
    """

    def __init__(self, bit=None, parser_instance=None):
        super(SimpleUnit, self).__init__(bit, parser_instance)
        self.synthesis()
