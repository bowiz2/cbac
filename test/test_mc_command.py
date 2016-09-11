import unittest
from cbac.mc_command import MCCommand, SimpleCommand, LazyCommand


class TestMCCommand(unittest.TestCase):
    def setUp(self):
        self.command = MCCommand()

    def test_def(self):
        self.assertFalse(self.command.is_conditional)

    def test_other_init(self):
        self.command = MCCommand(True)
        self.assertTrue(self.command.is_conditional)

    def test_compile(self):
        self.assertRaises(AssertionError, self.command.compile)


class TestSimpleCommand(unittest.TestCase):
    def test_init(self):
        command = SimpleCommand("/say Hello World", True)
        self.assertTrue(command.is_conditional)
        self.assertEqual("/say Hello World", command.compile())


class TestLazyCommand(unittest.TestCase):
    def setUp(self):
        self.undef = None

        def foo(a, b, c):
            undef = self.undef
            return "/say {} {} {} {}".format(a, b, c, len(undef))

        self.lazy_command = LazyCommand(foo, True, "1", "2", c="12387")

    def test_compile(self):
        self.undef = [1, 2, 34, 5]
        expected_result = "/say 1 2 12387 4"
        self.assertEqual(expected_result, self.lazy_command.compile())