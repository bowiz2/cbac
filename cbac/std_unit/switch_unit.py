"""Holds example unit"""
from cbac.unit import auto_synthesis
from cbac.unit.unit_base import Unit
from cbac.unit.statements import *
from cbac import std_logic
from cbac.core.compound import CBA


class SwitchUnit(Unit):
    """
    Switches between two units
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()
    @auto_synthesis
    def __init__(self, conditions, true_unit, false_unit):
        super(SwitchUnit, self).__init__(0)
        # == Here SwitchUnit declare all your memory slots.
        self.conditions = conditions
        self.true_unit = true_unit
        self.false_unit = false_unit

        self.callback_vortex = self.add_compound(CBA(self.shell.activate()))

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        yield If(self.conditions).then(
            self.true_unit.callback_pivot.tp(self.callback_vortex),
            self.true_unit.shell.activate()
        ).otherwise(
            self.false_unit.callback_pivot.tp(self.callback_vortex),
            self.false_unit.shell.activate()
        )
