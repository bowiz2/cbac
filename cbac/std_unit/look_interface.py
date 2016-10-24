"""Holds example unit"""
from cbac.unit import auto_synthesis
from cbac.unit.unit_base import Unit
from cbac import std_logic
from cbac.core.utils import Vector
from math import acos, degrees
from cbac import std_unit
from cbac.core import mc_command
import math


def angle (a, b, c):
    return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))


class LookPlane(object):
    def __init__(self, location, size):
        """
        :param location: relative to the player.
        """
        self.location = location
        self.size = size

    def get_look_boundries(self, looking_position):
        looking_position = looking_position + Vector(0, 1.62, 0)
        bottom = self.location
        top = self.location + self.size
        m_range_horizontal = []
        m_range_vertical = []
        for i in [bottom, top]:
            work = i - looking_position
            a = work.z
            c = work.x
            b = math.sqrt((a**2) + (c**2))
            m_range_horizontal.append(angle(a, b, c))
            work = i - looking_position
            a = work.z
            c = work.y
            b = math.sqrt((a ** 2) + (c ** 2))
            m_range_vertical.append(angle(a, b, c))
        return m_range_vertical, m_range_horizontal


class LookInterfaceUnit(Unit):
    """
    This is an example of a basic structure of a command block array unit.
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()

    @auto_synthesis
    def __init__(self, player, player_location, look_planes, interface_schematic=None):
        super(LookInterfaceUnit, self).__init__(0)
        self.player = player
        self.player_location = player_location
        self.look_planes = look_planes
        #self.interface_schematic = self.add_compound(interface_schematic)
        self.listners = []
        for plain in self.look_planes:
            vertical, horizontal = plain.get_look_boundries(self.player_location)
            vertical_listner = self.add_unit(std_unit.Listener(player.shell.test_rotation_vertical(int(min(vertical)), int(max(vertical))), mc_command.say("plain match for" + str(plain))))
            self.listners.append(vertical_listner)


    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        yield mc_command.say("hoooo")

