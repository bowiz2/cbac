import cpu8051.opcode
from cpu8051.handlers.handler import Handler


class _AddHandler(Handler):

    @property
    def logic_unit(self):
        return self.cpu.adder_unit


class AddARxHandler(_AddHandler):
    """
    ADD A, RX
    """
    opcode_set = cpu8051.opcode.add_a_rx

    def handle(self, opcode_value=None):
        for yield_out in self.make_logic(self.get_register(opcode_value)):
            yield yield_out


class AddADirectHandler(_AddHandler):
    """
    ADD A, direct
    """
    opcode_set = cpu8051.opcode.add_a_rx

    def handle(self, _=None):
        yield self.cpu.address_fetcher.shell.activate()
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.read_unit.shell.activate(),
            self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                *self.make_logic(self.cpu.read_unit.read_output)
            ))
        ))


class AddARiHandler(_AddHandler):
    """
    ADD A, @Ri
    """
    opcode_set = cpu8051.opcode.add_a_ri

    def handle(self, opcode_value=None):
        yield self.get_register(opcode_value).shell.copy(self.cpu.read_unit.address_input)
        yield self.cpu.read_unit.shell.activate()
        yield self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
            *self.make_logic(self.cpu.read_unit.read_output)
        ))


class AddADataHandler(_AddHandler):
    """
    ADD A, data
    """
    opcode_set = cpu8051.opcode.add_a_data

    def handle(self, _=None):
        yield self.cpu.accumulator.shell.copy(self.cpu.adder_unit.input_a)
        yield self.cpu.second_fetcher.shell.activate()
        yield self.cpu.second_fetcher.callback_pivot.shell.tp(
            self.cpu.procedure(*self.make_logic(self.cpu.process_registers[1]))
        )


add_handlers = [AddADirectHandler, AddARxHandler, AddADataHandler, AddARiHandler]