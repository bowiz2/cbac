from test_std_unit import StdUnitTestCase, named_schematic
from cpu8051.body import Cpu8051
import cpu8051.handlers.mov
from cpu8051 import opcode


class TestCpu(StdUnitTestCase):
    @named_schematic
    def test_body(self):
        self.block_space.add_unit(Cpu8051())

    @named_schematic
    def test_inc_iram(self):
        memory = [0] * 256
        inc_target = 0x03

        memory[0] = opcode.INC_IRAM
        memory[1] = inc_target
        memory[inc_target] = 0x01

        self.block_space.add_unit(Cpu8051(memory))

    @named_schematic
    def test_mov(self):
        cpu = Cpu8051(auto_synthesis=False)
        mov_a_rx = cpu8051.handlers.mov.MovARx(cpu)
        self.block_space.add_unit(cpu, mov_a_rx)