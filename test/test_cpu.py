from test.test_std_unit import StdUnitTestCase, named_schematic


class TestCpu(StdUnitTestCase):
    @named_schematic
    def test_cpu_partial(self):
        