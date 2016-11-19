from test_std_unit import StdUnitTestCase, named_schematic
from cpu8051.body import Cpu8051
import cpu8051.handlers.mov
from cpu8051 import opcode
from cbac.shortcuts import procedure
import random
from cbac.core import mc_command


class TestCpu(StdUnitTestCase):
    @named_schematic
    def test_body(self):
        self.block_space.add_unit(Cpu8051())


    @named_schematic
    def test_mov_a_rx(self):
        cpu = Cpu8051(auto_synthesis=False)
        mov_a_rx = cpu8051.handlers.mov.MovARx(cpu)

        random_move = random.choice(mov_a_rx.opcodes)

        self.block_space.add(procedure("register_layout").body(
            mc_command.say("chosen MOV A, R{}".format(mov_a_rx.get_arg(random_move, 'r'))),
            cpu.constant_factory(random_move).shell.copy(cpu.process_registers[0]),
            *[cpu.constant_factory(i).shell.copy(cpu.general_registers[i]) for i in xrange(8)]
        ))

        self.block_space.add_unit(cpu, mov_a_rx)


