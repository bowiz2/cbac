"""
Modes are the diffrent fetch processes used for the execution of an opcode
for exanple a, direct

a, rn

and so fourth.

This thing is convoluted and weird as the tax code.
WORNING!!!! IAMOND INHERITANCE IS IN PLACE!!!1
"""
# Each mode in here will be descriped of the operators creating the mode.
# For example The mode "DirectDataMode" is the mode of the opcode ANL direct, data


class Mode(object):
    """
    Mode is a behaviour of a handler.
    """
    @property
    def acting_registers(self):
        """
        Means it is automaticly fetches these registers without commands.
        :return:
        """
        return []

    @property
    def store_register(self):
        """
        The register to which the memory will be written to.
        :return:
        """
        return self.acting_registers[0]

    def preppend_actor(self, mode_type, *actors):
        return list(actors) + super(mode_type, self).acting_registers

    @property
    def logic_unit(self):
        """
        Must be implemented if make_logic is used.
        """
        raise NotImplementedError()

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

    def behaviour(self, opcode_value=None):
        raise NotImplementedError()


class RxMode(Mode):
    """
    Any handler which handles opcode of the type
    OPCODE A, RX
    should derive from this class.
    """

    @property
    def acting_registers(self):
        return self.preppend_actor(RxMode, self.handled_register)

    def behaviour(self, opcode_value=None):
        """
        Handlers mode which uses a and rn register opcodes.
        """
        self.handled_register = self.get_register(opcode_value)
        for yield_out in self.make_logic(*self.acting_registers):
            yield yield_out


class DirectMode(Mode):
    @property
    def acting_registers(self):
        self.direct_register_hold = self.cpu.read_unit.read_output
        return self.preppend_actor(DirectMode, self.direct_register_hold)

    def make_logic(self, register_a=None, register_b=None):
        # Deside if we need to store the result of the logic inside the memory or
        if self.store_register == self.direct_register_hold:
            yield register_a.shell.copy(self.logic_unit.inputs[0])
            yield register_b.shell.copy(self.logic_unit.inputs[1])
            yield self.logic_unit.shell.activate()
            yield self.logic_unit.callback_pivot.shell.tp(self.cpu.procedure(
                self.logic_unit.outputs[0].shell.store_to_temp(),
                self.cpu.access_unit.pivot.shell.load_from_temp(self.logic_unit.outputs[0]),
                self.cpu.done_opcode.shell.activate()
            ))
        else:
            for yield_out in super(DirectMode, self).make_logic(register_a, register_b):
                yield yield_out

    def behaviour(self, _=None):
        """
        Handles a single opcode.
        """
        if self.store_register == self.direct_register_hold:
            yield self.cpu.address_fetcher.shell.activate()
            yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                self.cpu.read_unit.shell.activate(),
                self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                    *self.make_logic(self.cpu.read_unit.read_output, self.cpu.accumulator)
                ))
            ))
        else:
            yield self.cpu.address_fetcher.shell.activate()
            yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                self.cpu.read_unit.shell.activate(),
                self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                    *self.make_logic(*self.acting_registers)
                ))
            ))


class RiMode(Mode):
    @property
    def acting_registers(self):
        return self.preppend_actor(RiMode, self.cpu.read_unit.read_output)

    def behaviour(self, opcode_value=None):
        """
        Handler all the opcodes which uses a register an RN register.
        :param opcode_value: the opcode we need to handle.
        """
        yield self.get_register(opcode_value).shell.copy(self.cpu.read_unit.address_input)
        yield self.cpu.read_unit.shell.activate()
        yield self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
            *self.make_logic(*self.acting_registers)
        ))


class DataMode(Mode):
    @property
    def acting_registers(self):
        return self.preppend_actor(DataMode, self.cpu.process_registers[1])

    def behaviour(self, _=None):
        """
        Handlers a single opcode.
        """
        yield self.cpu.accumulator.shell.copy(self.cpu.adder_unit.input_a)
        yield self.cpu.second_fetcher.shell.activate()
        yield self.cpu.second_fetcher.callback_pivot.shell.tp(
            self.cpu.procedure(*self.make_logic(*self.acting_registers))
        )


class DirectDataMode(DirectMode):
    """
    Any handler which handles opcode of the type
    OPCODE direct, data
    should derive from this class.
    """

    @property
    def acting_registers(self):
        return self.preppend_actor(DirectDataMode, self.cpu.process_registers[1])

    def behaviour(self, _=None):
        """
        Handlers a single opcode.
        """
        yield self.cpu.address_fetcher.shell.activate()
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.read_unit.shell.activate(),
            self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                self.cpu.second_fetcher.shell.activate(),
                self.cpu.second_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                    *self.make_logic(*self.acting_registers)
                ))
            ))
        ))


class DirectAMode(DirectMode):
    @property
    def acting_registers(self):
        return self.preppend_actor(DirectAMode, self.cpu.accumulator)


class AMode(Mode):
    @property
    def acting_registers(self):
        return self.preppend_actor(ARxMode, self.cpu.accumulator)


class ARxMode(AMode, RxMode):
    pass


class ADirectMode(AMode, DirectMode):
    """
    Any handler which handles opcode of the type
    OPCODE A, direct
    should derive from this class.
    """
    pass


class ARiMode(AMode, RiMode):
    """
    Any handler which handles opcode of the type
    OPCODE A, @Ri
    should derive from this class.
    """
    pass


class ADataMode(AMode, DataMode):
    """
    Any handler which handles opcode of the type
    OPCODE A, data
    should derive from this class.
    """
    pass
