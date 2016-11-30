from cpu8051.handlers.handler import Handler
import cpu8051.opcode


class _AddHandler(Handler):

    @property
    def adder(self):
        return self.cpu.adder_unit

    def make_add(self, register):
        yield self.cpu.accumulator.shell.copy(self.adder.input_a)
        yield register.shell.copy(self.adder.input_b)
        yield self.adder.shell.activate()
        yield self.adder.callback_pivot.shell.tp(self.cpu.procedure(
            self.adder.output.shell.copy(self.cpu.accumulator),
            self.cpu.done_opcode.shell.activate()
        ))


class AddARxHandler(_AddHandler):
    """
    ADD A, RX
    """
    opcode_set = cpu8051.opcode.add_a_rx

    def handle(self, opcode_value=None):
        for yield_out in self.make_add(self.get_register(opcode_value)):
            yield yield_out


class AddADirectHandler(_AddHandler):
    """
    ADD A, direct
    """
    opcode_set = cpu8051.opcode.add_a_rx

    def handle(self, _=None):
        yield self.cpu.address_fetcher.shell.activate()
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(
            self.cpu.procedure(
                self.cpu.read_unit.shell.activate(),
                self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                    *self.make_add(self.cpu.read_unit.output)
            ))
        ))


class AddRiHandler(_AddHandler):
    """
    ADD A, @Ri
    """
    opcode_set = cpu8051.opcode.add_a_ri

    def handle(self, opcode_value=None):
        for yield_out in self.make_add(self.get_register(opcode_value)):
            yield yield_out


class AddADataHandler(_AddHandler):
    """
    ADD A, data
    """
    opcode_set = cpu8051.opcode.add_a_data

    def handle(self, _=None):
        yield self.cpu.accumulator.shell.copy(self.cpu.adder_unit.input_a)
        yield self.cpu.second_fetcher.shell.activate()
        yield self.cpu.second_fetcher.callback_pivot.shell.tp(
            self.cpu.procedure(*self.make_add(self.cpu.process_registers[1]))
        )

