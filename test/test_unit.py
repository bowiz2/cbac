"""
Tests for the unit class. mainly unit statemtns.
"""
from unittest import TestCase

from cbac.core.command_shell.command_suspender import CommandSuspender
from cbac.core.compound import Register
from cbac.unit import Unit, SimpleUnit
from cbac.unit import auto_synthesis
from cbac.unit.logic_parser import UnitLogicParser, CommandCollection
from cbac.unit.statements import *
from cbac import std_logic
from test.decorators import named_schematic
from test_std_unit import StdUnitTestCase
from test.utils import open_products


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


class TestCallback(StdUnitTestCase):
    @named_schematic
    def test_callback(self):
        class A(SimpleUnit):
            def architecture(self):
                yield "/say im body"

        a = A()

        class B(SimpleUnit):
            def architecture(self):
                yield "/say im begin"
                yield MainLogicJump(a)
                yield "/say im end"

        self.block_space.add_unit(a)
        self.block_space.add_unit(B())

    @named_schematic
    def test_otherwise(self):

        class Dummy(Unit):
            def architecture(self):
                from cbac import Player
                yield If(Player(name="NotDude").shell.test_exists()).then(
                    mc_command.say("Dude exist!")
                ).otherwise(
                    mc_command.say("Dude does not exist!")
                )

        dummy = Dummy()
        dummy.synthesis()
        self.block_space.add_unit(dummy)


class TestUnitStatementsParsing(TestLogicParser):
    """
    Test the statement parsing.
    """

    def test_if(self):
        subject_shell = Register(2).blocks[0].shell


        If(self.sample_condition_command).then(
            self.sample_command,
            self.other_sample_command
        ).parse(self.parser)

        self.assertTrue(all([item.__class__ in [CommandSuspender, str] for item in self.parser.parse_stack[1:]]))
        self.assertIsInstance(self.parser.parse_stack[0], Conditional)

    def test_command(self):
        Command("/say hello").parse(self.parser)
        command = self.parser.commands[0]
        self.assertEqual("/say hello", command.compile())

    def test_inline_call(self):
        called_unit = Unit(4)
        InlineCall(called_unit).parse(self.parser)

    def test_main_logic_jump(self):
        class DummyUnit(SimpleUnit):
            """
            Unit which is used for testing
            """
            def architecture(self):
                """
                just say hey
                """
                yield "/say hey"

        dummy_unit = DummyUnit()
        MainLogicJump(dummy_unit).parse(self.parser)
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

    def test_truth_table(self):
        a = std_logic.In()
        b = std_logic.In()
        c = std_logic.Out()

        TruthTable([
            [[a, b], [c]],
            [[0, 0], [1]],
            [[1, 1], [1]],
            [[1, 0], [0]],
        ]).parse(self.parser)

        self.assertEqual(len(self.parser.parse_stack), 2)



class TestCommandCollection(TestCase):
    def test_init(self):
        collection1 = CommandCollection()
        collection2 = CommandCollection()

        my_dict = dict()

        my_dict[collection1] = "a"
        my_dict[collection2] = "b"

        self.assertEqual("a", my_dict[collection1])
        self.assertEqual("b", my_dict[collection2])
