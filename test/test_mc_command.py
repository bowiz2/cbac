import unittest

from cbac.core.mc_command import MCCommand, SimpleCommand, LazyCommand, factory, MCCommandFactoryError


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

        self.lazy_command = LazyCommand(foo, True, False, "1", "2", c="12387")

    def test_compile(self):
        self.undef = [1, 2, 34, 5]
        expected_result = "/say 1 2 12387 4"
        self.assertEqual(expected_result, self.lazy_command.compile())


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.sample_command = "/say hello"

    def test_regular(self):
        result = factory(self.sample_command)
        self.assertFalse(result.is_conditional)
        self.assertFalse(result.creates_condition)
        self.assertTrue(self.sample_command, result.compile())

    def test_condtional(self):
        result = factory("?" + self.sample_command)
        self.assertTrue(result.is_conditional)

    def test_creates_condition(self):
        result = factory("?!" + self.sample_command)
        self.assertTrue(result.is_conditional)
        self.assertTrue(result.creates_condition)
        result = factory("!?" + self.sample_command)
        self.assertTrue(result.is_conditional)
        self.assertTrue(result.creates_condition)

    def test_error(self):
        self.assertRaises(MCCommandFactoryError, factory, "! say hello")
        self.assertRaises(MCCommandFactoryError, factory, "1/say hello")
