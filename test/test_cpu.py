from cpu8051.body import Cpu8051
from cpu8051.handlers import all_handlers
from test.test_std_unit import StdUnitTestCase, named_schematic


class TestCpu(StdUnitTestCase):
    @named_schematic
    def test_cpu_partial(self):
        cpu = Cpu8051(auto_synthesis=False)
        cpu.handlers = map(lambda x: x(cpu, debug=True), all_handlers)
        for handler in cpu.handlers:
            cpu.add_unit(handler)
        cpu.synthesis()
        self.block_space.add_unit(cpu)