from cbac.unit import Unit
import functools
from sul.simple_array import SimpleArray
from cbac.unit import std_logic


class Gate(Unit):
    """
    A gate is a unit which can be composed into arrays.
    """
    @property
    @classmethod
    def array(cli):
        """
        :return: Array constructor function.
        """
        register_types = []
        for port in self.ports:

        functools.partial(SimpleArray, cli, [])