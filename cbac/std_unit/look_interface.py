"""Holds look interface."""
from cbac.unit import auto_synthesis
from cbac.unit.unit_base import Unit
from cbac import std_logic
from cbac.core.utils import Vector
from math import acos, degrees
from cbac import std_unit
from cbac.core import mc_command
import math
from cbac.unit.statements import *


# TODO: Refactor to  be reasonable quality


def angle(a, b, c):
    """
    Calculate the angle between a b and c in a trinangle.
    :param a:
    :param b:
    :param c:
    :return:
    """
    return math.degrees(math.acos((c ** 2 - b ** 2 - a ** 2) / (-2.0 * a * b)))


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
            b = math.sqrt((a ** 2) + (c ** 2))
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
    I wrote this when I was drunk...
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()

    @auto_synthesis
    def __init__(self, bits, player, player_location, look_planes, output=std_logic.OutputRegister):
        super(LookInterfaceUnit, self).__init__(bits)
        self.callback_pivot = None
        self.player = player
        self.player_location = player_location
        self.look_planes = look_planes
        self.resetter = std_unit.ListenerReSetter([])
        self.listners = []
        self.resetter.listeners = self.listners

        self.output = self.add_output(output)

    def architecture(self):
        """
        Ticks the view handler once
        """
        for plain_code, plain in self.look_planes.items():
            vertical, horizontal = plain.get_look_boundries(self.player_location)
            yield If([
                self.player.shell.test_rotation_vertical(int(min(vertical)), int(max(vertical))),
                self.player.shell.test_rotation_vertical(int(min(horizontal)), int(max(horizontal)))
            ]).then(self.constant_factory(plain_code).shell.copy(self.output))


default_keyboard_layout = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['\t', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\n'],
    ['z', 'x', 'v', 'b', 'n', 'm', ',', '.', '/']
]


class KeyboardInterfaceUnit(LookInterfaceUnit):
    def __init__(self, player, player_location, layout=default_keyboard_layout):
        look_planes = {}
        for y, row in enumerate(default_keyboard_layout):
            for x, char in enumerate(row):
                look_planes[ord(char)] = LookPlane(Vector(x, y, 0), size=Vector(1, 1, 1))
        super(KeyboardInterfaceUnit, self).__init__(8, player, player_location, look_planes)
