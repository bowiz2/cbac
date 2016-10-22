"""
This is similar to unittest's test case.
see example.py for example
"""
import inspect
import math

import assembler
from cbac import BlockSpace, Unit
from cbac.unit.statements import *
from mctest.assertion import Assertion
from sul import IncrementUnit


# TODO: auto deploy


class TesterUnit(Unit):
    """
    This is a unit which tests if a test passes or not.
    And contains all the in-game logic.
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

    def architecture(self):
        for action in self.actions:
            if isinstance(action, Assertion):
                assertion = action
                yield If(assertion.command).then(
                    STDCall(self.incrementer, self.success_count_register)
                )
                yield If(assertion.command).then(
                    "/say assertion ok"
                )
                yield If(assertion.command).then(
                    self.incrementer.output.shell.copy(self.success_count_register)
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
        # used in the setup and tear down.
        self.processed_method_name = None

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
            self.processed_method_name = method_name
            self.actions += list(self.setUp())
            unbound = unbound_method(self)
            if unbound:
                self.actions += list(unbound)
            self.actions += list(self.tearDown())

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

        schematic = assembler.build(self.blockspace)
        schematic.saveToFile(path)

    def setUp(self):
        """
        Will be added to the statements and executed before each.
        """
        yield "/say start {0} : {1}".format(self.__class__.__name__, self.processed_method_name)

    def tearDown(self):
        """"
        Will be executed and statements added after each function.
        """
        yield "/say end {0} : {1}".format(self.__class__.__name__, self.processed_method_name)

    def add_unit(self, unit):
        self.blockspace.add_unit(unit)
