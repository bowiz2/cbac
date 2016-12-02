"""
Contains all the abstract handler declaration and handler modes.
"""
import cbac
import cpu8051
from cbac.unit.statements import If
from cbac.core import mc_command


class Handler(cbac.unit.Unit):
    """
    Handles a specific opcode in the cpu.
    """
    opcode_set = None  # type: cpu8051.opcode.OpcodeSet

    @cbac.unit.auto_synthesis
    def __init__(self, cpu_body, debug=False):
        super(Handler, self).__init__(bits=cpu_body.bits)
        assert isinstance(cpu_body, cpu8051.body.Cpu8051)
        self.cpu = cpu_body
        self._debug = debug

    def get_register(self, value):
        """
        :return: get the register encoded in the opcode.
        """
        assert self.opcode_set, "must have opcode set."
        return self.cpu.general_registers[self.opcode_set.get_arg(value, 'r')]

    def handle(self, opcode_value=None):
        """
        This architecture will be generated for each opcode in the opcode set.
        :param opcode_value: Here will be passed the currently generated opcode. can be ignored if opcode set size is 1.
        :return: Generator which is an architecture which describes how to behave depending on the opcode.
        """
        yield None

    def architecture(self):
        """
        Descripes the architecture of the handler.
        :return:
        """
        if self._debug:
            yield mc_command.say("{} entry".format(self.__class__.__name__))

        for opcode in self.opcode_set.all():
            yield If(self.cpu.opcode_is(opcode)).then(
                *list(self.handle(opcode))
            )

    @property
    def logic_unit(self):
        """
        Must be implemented if make_logic is used.
        """
        raise NotImplemented()

    def make_logic(self, register_a=None, register_b=None):
        """
        see logic_unit property.
        :param register_a:
        :param register_b:
        :return:
        """
        if register_a:
            yield self.cpu.accumulator.shell.copy(self.logic_unit.inputs[0])
        if register_b:
            yield register_b.shell.copy(self.logic_unit.inputs[1])

        yield self.logic_unit.shell.activate()
        yield self.logic_unit.callback_pivot.shell.tp(self.cpu.procedure(
            self.logic_unit.outputs[0].shell.copy(self.cpu.accumulator),
            self.cpu.done_opcode.shell.activate()
        ))


class ARxMode(Handler):
    """
    Any handler which handles opcode of the type
    OPCODE A, RX
    should derive from this class.
    """

    def handle(self, opcode_value=None):
        """
        Handlers mode which uses a and rn register opcodes.
        """
        for yield_out in self.make_logic(self.cpu.accumulator, self.get_register(opcode_value)):
            yield yield_out


class ADirectMode(Handler):
    """
    Any handler which handles opcode of the type
    OPCODE A, direct
    should derive from this class.
    """

    def handle(self, _=None):
        """
        Handles a single opcode.
        """
        yield self.cpu.address_fetcher.shell.activate()
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.read_unit.shell.activate(),
            self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                *self.make_logic(self.cpu.accumulator, self.cpu.read_unit.read_output)
            ))
        ))


class ARiMode(Handler):
    """
    Any handler which handles opcode of the type
    OPCODE A, @Ri
    should derive from this class.
    """

    def handle(self, opcode_value=None):
        """
        Handler all the opcodes which uses a register an RN register.
        :param opcode_value: the opcode we need to handle.
        """
        yield self.get_register(opcode_value).shell.copy(self.cpu.read_unit.address_input)
        yield self.cpu.read_unit.shell.activate()
        yield self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
            *self.make_logic(self.cpu.accumulator, self.cpu.read_unit.read_output)
        ))


class ADataMode(Handler):
    """
    Any handler which handles opcode of the type
    OPCODE A, data
    should derive from this class.
    """
    opcode_set = cpu8051.opcode.add_a_data

    def handle(self, _=None):
        """
        Handlers a single opcode.
        """
        yield self.cpu.accumulator.shell.copy(self.cpu.adder_unit.input_a)
        yield self.cpu.second_fetcher.shell.activate()
        yield self.cpu.second_fetcher.callback_pivot.shell.tp(
            self.cpu.procedure(*self.make_logic(self.cpu.accumulator, self.cpu.process_registers[1]))
        )


class DirectAMode(Handler):
    """
    Any handler which handles opcode of the type
    OPCODE direct, a
    should derive from this class.
    """

    def make_logic(self, register_a=None, register_b=None):
        """
        see logic_unit property.
        :param register_a:
        :param register_b:
        :return:s
        """
        input_a = self.logic_unit.inputs[0]
        input_b = self.logic_unit.inputs[1]
        output = self.logic_unit.outputs[0]
        yield self.cpu.accumulator.shell.copy(input_a)
        yield register_b.shell.copy(input_b)
        yield self.logic_unit.shell.activate()
        yield self.logic_unit.callback_pivot.shell.tp(self.cpu.procedure(
            output.shell.store_to_temp(),
            self.cpu.access_unit.pivot.shell.load_from_temp(output)
        ))

    def handle(self, _=None):
        """
        Handles a single opcode
        """
        yield self.cpu.address_fetcher.shell.activate()
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.read_unit.shell.activate(),
            self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                *self.make_logic(self.cpu.read_unit.read_output, self.cpu.accumulator)
            ))
        ))


class DirectDataMode(DirectAMode):
    """
    Any handler which handles opcode of the type
    OPCODE direct, data
    should derive from this class.
    """
    def handle(self, _=None):
        """
        Handlers a single opcode.
        """
        yield self.cpu.address_fetcher.shell.activate()
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.read_unit.shell.activate(),
            self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                self.cpu.second_fetcher.shell.activate(),
                self.cpu.second_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                    *self.make_logic(self.cpu.read_unit.read_output, self.cpu.process_registers[1])
                ))
            ))
        ))
