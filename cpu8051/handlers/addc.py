import cpu8051.opcode
from cpu8051.handlers import AddARxHandler, AddADirectHandler
from cbac.unit.statements import If


class AddcARxHandler(AddARxHandler):
    opcode_set = cpu8051.opcode.addc_a_rx

    def handle(self, opcode_value=None):
        yield If(self.cpu.carry_flag.shell == True).then(
            self.cpu.adder_unit.carry.ports[0].shell.activate()
        )
        yield If(self.cpu.auxiliary_carry_flag.shell == True).then(
            self.cpu.adder_unit.carry.ports[0].shell.activate()
        )

        for yield_out in super(AddcARxHandler, self).handle(opcode_value):
            yield yield_out


class AddcADirectHandler(AddADirectHandler):
    opcode_set = cpu8051.opcode.addc_a_direct

    def handle(self, opcode_value=None):
        yield If(self.cpu.carry_flag.shell == True).then(
            self.cpu.adder_unit.carry.ports[0].shell.activate()
        )
        yield If(self.cpu.auxiliary_carry_flag.shell == True).then(
            self.cpu.adder_unit.carry.ports[0].shell.activate()
        )

        for yield_out in super(AddcADirectHandler, self).handle(opcode_value):
            yield yield_out