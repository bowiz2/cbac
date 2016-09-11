import unittest
from cbac.mc_command import MCCommand, SimpleCommand


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

