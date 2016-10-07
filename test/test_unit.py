"""
Tests for the unit class. mainly unit statemtns.
"""
from unittest import TestCase
from cbac.unit import Unit, SimpleUnit
from cbac.unit import std_logic, auto_synthesis
from cbac.unit.statements import *
from cbac.compound import Register, Constant
from cbac.command_shell.command_suspender import CommandSuspender
import cbac.config
from cbac.unit.logic_parser import UnitLogicParser, CommandCollection
from test_sul import SULTestCase
from test.decorators import named_schematic


class TestUniProperties(TestCase):
    def test_ports_signature(self):
        class SampleUnit(Unit):
            @auto_synthesis
            def __init__(self, a=std_logic.In, b=std_logic.In, s=std_logic.Out):
                super(SampleUnit, self).__init__()
                self.a = self.add(a)
                self.b = self.add(b)
                self.s = self.add(s)

        self.assertEqual(len(SampleUnit.ports_signature()), 3, "unexpected size")
        self.assertEqual(SampleUnit.ports_signature()[0], std_logic.In)
        self.assertEqual(SampleUnit.ports_signature()[1], std_logic.In)
        self.assertEqual(SampleUnit.ports_signature()[2], std_logic.Out)


class TestLogicParser(TestCase):
    def setUp(self):
        self.parser = UnitLogicParser()
        # used for statement which require commands.
        self.sample_command = "/say sample command"
        # used for statements which require multiple commands.
        self.other_sample_command = "/say other sample command"

        self.sample_condition_command = Register(1).blocks[0].shell == True

    def test_parse(self):
        pass

    def test_eat(self):
        pass

    def test_parse_cllection(self):
        pass

    def test_parsed_suspended_command(self):
        dummy = Register(3)
        self.parser.add_parsed(dummy.shell.reset())
        self.assertIsInstance(self.parser.commands[0], CommandSuspender)

    def test_parsed_invalid(self):
        self.assertRaises(AssertionError, self.parser.add_parsed, [])


class TestCallback(SULTestCase):
    @named_schematic
    def test_callback(self):
        class A(SimpleUnit):
            def architecture(self):
                yield "/say im a"

        a = A()

        class B(SimpleUnit):
            def architecture(self):
                yield "/say im b first"
                yield MainLogicJump(a)
                yield "/say im b last"

        print a.logic_cbas
        self.block_space.add_unit(a)
        self.block_space.add_unit(B())


class TestUnitStatementsParsing(TestLogicParser):
    """
    Test the statement parsing.
    """

    def test_switch(self):
        target_register = Register(8)
        some_constant = Constant(31)

        self.parser.parse_statement(Switch(target_register).by(
            case[0](
                target_register.shell.reset()
            ),
            case[1](
                target_register.shell.fill(0)
            ),
            case[2](
                target_register.shell.copy(some_constant)
            )

        ))
        for frame in self.parser.parse_stack:
            self.assertIsInstance(frame, If)

    def test_if(self):
        subject_shell = Register(2).blocks[0].shell

        self.parser.parse_statement(
            If(self.sample_condition_command).then(
                self.sample_command,
                self.other_sample_command
            )
        )
        self.assertTrue(all([item.__class__ in [CommandSuspender, str] for item in self.parser.parse_stack[1:]]))
        self.assertIsInstance(self.parser.parse_stack[0], Conditional)

    def test_command(self):
        self.parser.parse_statement(Command("/say hello"))
        command = self.parser.commands[0]
        self.assertEqual("/say hello", command.compile())

    def test_inline_call(self):
        called_unit = Unit(4)
        self.parser.parse_statement(InlineCall(called_unit))

    def test_debug(self):
        cbac.config.DEBUG_BUILD = True
        self.parser.parse_statement(Debug("/say hello"))
        self.assertEqual(1, len(self.parser.parse_stack))
        self.assertEquals(self.parser.parse_stack[0], "/say hello")

    def test_debug_off(self):
        cbac.config.DEBUG_BUILD = False
        self.parser.parse_statement(Debug("/say hello"))
        self.assertEqual(0, len(self.parser.parse_stack))

    def test_main_logic_jump(self):
        class DummyUnit(SimpleUnit):
            def architecture(self):
                yield "/say hey"

        dummy_unit = DummyUnit()
        self.parser.parse_statement(MainLogicJump(dummy_unit))
        # Check internal state.
        self.assertEqual(2, len(self.parser.all_commands))
        self.assertEqual(1, len(self.parser.jumps))

    def test_main_logic_jump_full(self):
        class DummyUnit(SimpleUnit):
            def architecture(self):
                yield "/say hey"

        dummy_unit = DummyUnit()
        logic_cbas, other_compounds, other_units = self.parser.parse([MainLogicJump(dummy_unit)])
        self.assertEqual(2, len(logic_cbas))


class TestCommandCollection(TestCase):
    def test_init(self):
        collection1 = CommandCollection()
        collection2 = CommandCollection()

        my_dict = {}

        my_dict[collection1] = "a"
        my_dict[collection2] = "b"

        self.assertEqual("a", my_dict[collection1])
        self.assertEqual("b", my_dict[collection2])
