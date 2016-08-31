from unittest import TestCase

import cbac.compound.cba
import cbac.compound.padder
from cbac.block import CommandBlock
from cbac.compound.padder import PadBlock


class ConditionalMock(object):
    """
    Used in the padding test.
    """

    def __init__(self, is_conditional=True):
        self.is_conditional = is_conditional

    def __str__(self):
        return "ConditionalMock"


class CreatesConditionMock(object):
    """
    Used in the padding test.
    """

    def __init__(self, creates_condition=True):
        self.creates_condition = creates_condition

    def __str__(self):
        return "CreatesConditionMock"


class TestPedder(TestCase):
    def setUp(self):
        self.creates = CommandBlock(CreatesConditionMock())
        self.conditioned = CommandBlock(ConditionalMock())
        self.regular = CommandBlock("/say dummy command")

    def test_check_conditional(self):
        self.assertTrue(cbac.compound.padder.check_conditional(self.creates))
        self.assertTrue(cbac.compound.padder.check_conditional(self.conditioned))
        self.assertFalse(cbac.compound.padder.check_conditional(self.regular))

    def test_pad(self):
        def is_creates(obj):
            """
            Check if the object has condition creating commands
            """
            return obj is self.creates

        def is_conditioned(obj):
            """
            Check if object has a conditional command.
            """
            return obj is self.conditioned

        def is_regular(obj):
            """
            Check if object is regular
            """
            return obj is self.regular

        def is_padding(obj):
            """
            Check if obj is padding
            """
            return isinstance(obj, PadBlock)

        simple_case = (self.regular, self.regular, self.regular, self.regular, self.regular, self.regular)
        self.assertEqual(tuple(cbac.compound.padder.pad(simple_case.__iter__(), 4)), simple_case)

        complex_case = (
            self.creates, self.creates, self.creates, self.conditioned, self.conditioned, self.regular, self.regular)

        truth_checkers = (
            is_creates, is_creates, is_creates, is_padding, is_padding, is_conditioned, is_conditioned, is_regular,
            is_regular)

        results = tuple(cbac.compound.padder.pad(complex_case.__iter__(), 4))
        thruths = [checker(result_item) for checker, result_item in zip(truth_checkers, results)]
        self.assertTrue(all(thruths))

    def test_segments(self):
        bulk = (True, True, False, True, True, False, False, False)
        result = tuple(cbac.compound.padder.segments(bulk))
        excpected = ((True, True), (False,), (True, True), (False, False, False))
        self.assertEqual(excpected, result)
