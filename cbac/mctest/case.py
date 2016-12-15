"""
This is similar to unittest's test case.
see example.py for example
"""
import inspect
import math

import unittest

from cbac import Unit
from cbac.unit.statements import *
from core.blockspace.blockspace import BlockSpace
from mctest.assertion import Assertion
from cbac import std_logic
from cbac.unit import auto_synthesis


class _TesterUnit(Unit):
    """
    A unit which tests a single method in a test case.
    """

    @auto_synthesis
    def __init__(self, actions, method_name):
        """
        :param method_name: the name of the test method.
        :param actions: action of the test method.
        """
        super(_TesterUnit, self).__init__(0)
        self.method_name = method_name
        self.actions = actions
        assertion_count = len(self.assertions)
        self.flag_register = self.add(std_logic.OutputRegister(assertion_count + 1))
        self.assertion_flags = dict(zip(self.assertions, self.flag_register.ports))
        self.test_pass_flag = self.flag_register.ports[-1]

    @property
    def assertions(self):
        """
        The assertions made by the user.
        :return:
        """
        return filter(lambda x: isinstance(x, Assertion), self.actions)

    def architecture(self):
        for action in self.actions:
            if isinstance(action, Assertion):
                assertion = action
                yield If(assertion.commands).then(
                    self.assertion_flags[assertion].shell.activate()
                ).otherwise(
                    mc_command.say(assertion.message)
                )
            else:
                yield action
        yield If(self.flag_register == self.flag_register.max_value()).then(
            mc_command.say("All Assertion passed"),
            self.test_pass_flag.shell.activate()
        ).otherwise(
            mc_command.say("{} Failed".format(self.__class__.__name__)),
            *[If(flag == True).then(mc_command.say(assertion.msg)) for flag, assertion in self.assertion_flags.items()]
        )


def test_in_minecraft(self):
    "casues us to test this module in minecraft"
    self.assertTrue(True)


def mctest(f):
    def _wrapper(self, *args, **kwargs):
        actions = list(f(self, *args, **kwargs))
        tester_unit = _TesterUnit(actions, f.__name__)
        self.blockspace.add_unit(tester_unit)
        test_in_minecraft(self)
    _wrapper.__name__ = f.__name__
    return _wrapper


class McTestCase(unittest.TestCase):
    """
    Imulating unittest's TestCase
    """

    word_size = None
    blockspace = BlockSpace()

    _constant_cache = {}

    def add_unit(self, unit):
        if inspect.isclass(unit):
            unit = unit(self.word_size)
        self.blockspace.add_unit(unit)
        return unit

    def add(self, compound):
        self.blockspace.add(compound)
        return compound

    def constant_factory(self, value, word_size=None):
        from cbac import HardwareConstant

        if not word_size:
            word_size = self.word_size

        if value not in self._constant_cache:
            constant = HardwareConstant(value, word_size)
            self._constant_cache[value] = constant
            self.add(constant)

        return self._constant_cache[value]
