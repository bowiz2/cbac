"""Holds Detector unit"""
from cbac.unit import auto_synthesis
from cbac.unit.unit_base import Unit
from cbac.unit.statements import *
from cbac import std_logic
from cbac.core import mc_command
import math
import cbac


class ViewDetectorVerticalUnit(Unit):
    """
    Detects the direction a player is looking at.
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()
    @auto_synthesis
    def __init__(self, player, output=std_logic.OutputRegister):
        super(ViewDetectorVerticalUnit, self).__init__(int(math.ceil(math.log(len(xrange(-90, 89)), 2))))
        self.player = player
        self.output = self.add_output(output)

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        for i in xrange(-90, 89):
            j = i + 1
            m_range = i, j
            yield If(self.player.shell.test_rotation_vertical(*m_range)).then(
                self.constant_factory(i+90).shell.copy(self.output)
            )


class ViewDetectorHorizonatlUnit(Unit):
    """
    Detects the direction a player is looking at.
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()
    @auto_synthesis
    def __init__(self, player, output=std_logic.OutputRegister):
        super(ViewDetectorHorizonatlUnit, self).__init__(int(math.ceil(math.log(len(xrange(-180, 178)), 2))))
        self.player = player
        self.output = self.add_output(output)

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        for i in xrange(-180, 178):
            j = i + 1
            m_range = i, j
            yield If(self.player.shell.test_rotation_horizontal(*m_range)).then(
                self.constant_factory(i+180).shell.copy(self.output)
            )
