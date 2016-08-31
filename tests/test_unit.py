"""
Tests for the unit class. mainly unit statemtns.
"""
from unittest import TestCase
from cbac.unit import Unit
from cbac.unit.statements import *


class SubjectUnit(Unit):
    pass


class TestUnitStatements(TestCase):

    def test_switch(self):
        def test_main():
            Switch(self.input[0] == True).by(
                Case[](),
                Case().then(),
                Case().then()
            )


        SubjectUnit.main_logic_commands = test_main
