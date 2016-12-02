"""
Holds the Unit class.
"""
import inspect
import itertools

from cbac.core.command_shell import UnitShell
from cbac.core.utils import memoize
from cbac.unit.logic_parser import UnitLogicParser
from cbac.unit.statements import InlineCall
from cbac import std_logic
from cbac.core.compound.hardware_constant import HardwareConstant
from cbac.core.mcentity import Pivot


# TODO: implement caching
# TODO: add refcount for a unit. to know if it can be included as an inline.
# TODO: organize the class, mainly the methods.


class Unit(object):
    """
    Now imitates a VHDL module.
    """
    callback_pivot_home = HardwareConstant(1, 1)

    def __init__(self, bits=None, logic_parser_instance=None, no_reset=False):
        """
        Create a unit with an input base length.
        :param bits: The base length of the unit.
        :param no_reset: indicates that this unit will not reset its inputs and outputs.
        """
        if not logic_parser_instance:
            logic_parser_instance = UnitLogicParser()
        self.bits = bits
        self._logic_parser = logic_parser_instance
        self.compounds = []
        # keep track of the ports in the unit.
        self.ports = []
        self.inputs = []
        self.outputs = []
        # Units which are needed for this unit to function.
        self.dependent_units = []
        self.build_whitelist = []
        # Logic cbas are cbac which excecute the logic of the unit. the entry point is the first logic_cba
        self.logic_cbas = []
        self.is_inline = False
        self.is_synthesized = False
        self.no_reset = no_reset
        self.auto_callback = True

        self._hardware_constant_cache = {}
        self.callback_pivot = Pivot()

    def synthesis(self):
        """
        Takes the entry commands main logic commands and exit commands, and compiles them into a collection of CBAs.
        This collection is called logic_cbac.
        :return: None
        """

        logic_cbas, other_compounds, other_units = self._logic_parser.parse(
            itertools.chain(self.on_entry_commands(), self.architecture(), self.on_exit_commands())
        )
        # Add the CBAs to the unit.
        for parsed_item in logic_cbas + other_compounds:
            self.add_compound(parsed_item)
        for other_unit in other_units:
            self.add_unit(other_unit)
        self.logic_cbas = logic_cbas
        self.is_synthesized = True

    def on_entry_commands(self):
        """
        Generate the commands which are executed when the entry pointed activated.
        """
        if not self.no_reset:
            for output_memory in self.outputs:
                yield output_memory.shell.reset()

    def architecture(self):
        """
        A body associated with an entity declaration to describe the internal organization or operation of a design entity.
        An architecture body is used to describe the behavior, data flow, or structure of a design entity.
        """
        pass

    def on_exit_commands(self):
        """
        Generate the commands which will be called when the main activation of the entry point is finished.
        :return:
        """
        if not self.no_reset:
            for input_memory in self.inputs:
                yield input_memory.shell.reset()
        if self.callback_pivot:
            if self.auto_callback:
                yield self.callback_pivot.shell.activate()
            yield self.callback_pivot.shell.kill()
            yield self.callback_pivot.shell.summon(self.callback_pivot_home)

    def add(self, item):
        """
        VOODOO for synthetic sugar.
        Process the item and see if you can format it for the need of the unit.
        :param item:
        :return:
        """
        if inspect.isclass(item):
            # Auto gen std components
            if issubclass(item, std_logic.StdLogic):
                # In-case a class was supplied.
                if issubclass(item, std_logic.Register):
                    item = std_logic.Register(self.bits)
                elif issubclass(item, std_logic.Port):
                    item = std_logic.Port()
                else:
                    assert False, "Unexpected std_logic item"
            # Convert unit classes to Unit creators.
            elif issubclass(item, Unit):
                unit_class = item

                def unit_creator(*args, **kwargs):
                    """
                    The unit is wrapped withing this method. and this method is returned into the creation scope.
                    """
                    generated_unit = unit_class(*args, **kwargs)
                    self.add_unit(generated_unit)
                    return InlineCall(generated_unit)

                item = unit_creator

        # Process inputs and outputs.
        if isinstance(item, std_logic.StdLogic):
            if isinstance(item, std_logic.Register):
                item = self.add_compound(item)
        return item

    def add_compound(self, item):
        """
        Add a compound to the compound list, meaning it will be compiled with the unit.
        :return: the added compound.
        """
        self.compounds.append(item)
        return item

    def _remove_compound(self, item):
        """
        used in tests
        """
        self.compounds.remove(item)

    def add_unit(self, unit):
        """
        Adds a unit to the dependent unit list.
        :return: The added unit.
        """
        if inspect.isclass(unit):
            unit = unit(self.bits)
        self.dependent_units.append(unit)
        return unit

    def add_input(self, interface):
        """
        Set a register as an input for this unit. And return it.
        """
        interface = self.add(interface)
        self.inputs.append(interface)
        return interface

    def add_output(self, interface):
        """
        Sets a register as an output of this unit. And return it.
        """
        interface = self.add(interface)
        self.outputs.append(interface)
        return interface

    def _add_io(self, interface):
        """
        determine if the interface is input or output and use the correct function on it
        Note: internal use only for auto-generation. strongly discouraged.
        """
        if issubclass(interface, std_logic.InputRegister) or issubclass(interface, std_logic.InputRegister):
            return self.add_input(interface)
        elif issubclass(interface, std_logic.OutputRegister) or issubclass(interface, std_logic.OutputRegister):
            return self.add_output(interface)
        else:
            assert False, "Unexpected interface type"

    def constant_factory(self, value):
        """
        Create a hardware constant with a value 'value'
        :param value: value of the hardware constant.
        :return: HardwareConstant.
        """
        # If this constant was never accessed before, add it to the cache.
        if value not in self._hardware_constant_cache:
            self._hardware_constant_cache[value] = HardwareConstant(value, word_size=self.bits)
            # Add it to the unit.
            self.add_compound(self._hardware_constant_cache[value])

        # Get the constant from the cache.
        constant = self._hardware_constant_cache[value]
        return constant

    @classmethod
    def ports_signature(cls):
        """
        defiend by the default ports provided in the __init__ of the unit.
        :return: list of the classes of the ports.
        """
        signature = [port for port in cls.__init__.func_defaults if issubclass(port, std_logic.Port)]
        return signature

    @property
    def ticks(self):
        """

        :return: Number of mc ticks to preform the action of this unit.
        """
        # TODO: implement
        return -1

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
        """
        :return: Minecraft command interface.
        """
        return UnitShell(self)

    @classmethod
    def Array(cls, size=None):
        """
        Get the class of the hardware array of this unit if possible.
        Array in the hardware sense.
        If no size is provided, the class of a gate array of the correct type is provided,
        If a size was provided an instance with the supplied size will be provided.
        """
        pass

    def procedure(self, *commands):
        from cbac.core.compound import CBA
        commands = filter(lambda x: x is not None, commands)
        return self.add_compound(CBA(*commands))


class SimpleUnit(Unit):
    """
    A simple unit has no input/output registers. it only preforms logic.
    """

    def __init__(self, bit=None, parser_instance=None):
        super(SimpleUnit, self).__init__(bit, parser_instance)
        self.synthesis()
