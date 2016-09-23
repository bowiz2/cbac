"""
This is imulating unittest's test case.
"""
from cbac import BlockSpace, Constant, CommandBlockArray, Register, Unit
from cbac.unit.statements import *
from sul import IncrementUnit, FullAdderUnit
import cbac.mc_command
import cbac.assembler
import inspect
import math

# TODO: auto deploy


class Assertion(object):
    def __init__(self, assert_command):
        """
        :param assert_command: This command determins if the assert was sucsessfull or not.
        """
        self.command = assert_command


class TesterUnit(Unit):
    """
    This is a unit which tests if a test passes or not.
    """
    def __init__(self, actions):
        super(TesterUnit, self).__init__()
        self.actions = actions
        assertion_count = len(self.assertions)
        assertions_log = int(math.ceil(math.log(assertion_count))) + 1
        self.incrementer = self.add_unit(IncrementUnit(assertions_log))
        self.success_count_register = self.create_output(assertions_log)
        self.synthesis()

    @property
    def assertions(self):
        """
        The assertions made by the user.
        :return:
        """
        return [isinstance(item, Assertion) for item in self.actions]

    def main_logic_commands(self):
        for action in self.actions:
            if isinstance(action, Assertion):
                assertion = action
                yield If(assertion.command).then(
                    STDCall(self.incrementer, self.success_count_register)
                )
            else:
                yield action


class McTestCase(object):
    """
    Imulating unittest's TestCase
    """

    def __init__(self):
        self.incrementer = None
        self.actions = []
        self.units = []
        # compounds which were needed for assertions.
        self.compounds = []

        self.blockspace = BlockSpace((1000, 1000, 1000))

    def build(self, path):
        """
        Build the test and save it to a schematic.
        :param path: path to the file to which the schematic will be saved.
        :return:
        """
        # work the test functions.
        test_methods = filter(
            lambda (key, value): key.startswith("test_"),
            inspect.getmembers(self.__class__, predicate=inspect.ismethod))

        for pair in test_methods:
            method_name, unbound_method = pair
            self.setUp()
            unbound_method(self)
            self.tearDown()

        if len(self.actions) > 0:
            tester_unit = TesterUnit(self.actions)
            self.blockspace.add_unit(tester_unit)

            #
            # cmd_batch_2 = []
            # for block in cba1.blocks:
            #     if hasattr(block, "command"):
            #         if block.command in [assertion.command for assertion in self.assertions]:
            #             cmd_batch_2.append(block.shell.has_failed())
            #             cmd_batch_2.append("/say assertion faild")
            #
            # cba2 = CommandBlockArray(*cmd_batch_2)
            # self.compounds.append(cba2)
        for compound in self.compounds:
            self.blockspace.add(compound)
        self.blockspace.pack()
        self.blockspace.shrink()

        schematic = cbac.assembler.build(self.blockspace)
        schematic.saveToFile(path)

    def setUp(self):
        """
        Will be added to the statements and executed before each.
        """
        pass

    def tearDown(self):
        """"
        Will be executed and statements added after each function.
        """
        pass

    def add_unit(self, unit):
        self.blockspace.add_unit(unit)

    def assertTrue(self, block):
        """
        Check whenever a block is activated.
        :param block: Block
        :return: None
        """
        self.actions.append(Assertion(block.shell == True))

    def assertFalse(self, block):
        """
        Check whenever a block is deactivated.
        :param block: Block
        :return:None
        """
        self.actions.append(Assertion(block.shell == False))

    def assertEquals(self, register, value):
        """
        Checks whenever a value of a register equals a value.
        :param register: Register you are checking
        :param value: The expected value of the register.
        :return: None
        """
        const_to_compare = Constant(value)
        self.compounds.append(const_to_compare)
        self.actions.append(Assertion(register.shell == const_to_compare))


class Sample(McTestCase):
    def test_ram(self):
        adder = FullAdderUnit(4)
        self.add_unit(adder)
        self.assertEquals(adder.output, 0)
        num5 = Constant(5, 4)
        num3 = Constant(3, 4)
        self.blockspace.add(num5)
        self.blockspace.add(num3)
        self.actions.append(num5.shell.copy(adder.input_a))
        self.actions.append(num3.shell.copy(adder.input_b))
        self.actions.append(adder.activator.shell.activate())
        self.assertEquals(adder.output, 8)

s = Sample()
s.build("C:/temp/x.schm")