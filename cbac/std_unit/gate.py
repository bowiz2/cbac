from cbac.unit import Unit
from cbac.unit import auto_synthesis
from cbac import std_logic
from cbac.std_unit.simple_array import SimpleArray


class Gate(Unit):
    """
    A gate is a unit which can be composed into arrays.
    """

    @classmethod
    def Array(cls, size=None):
        """
        Array in the hardware sense.
        If no size is provided, the class of a gate array of the correct type is provided,
        If a size was provided an instance with the supplied size will be provided.


        meaning that the statement
            my_array_class = MyGate.Array()
            array_instance = my_array_class(8)
        is equal to
            array_instance = MyGate.Array()(8)
        is equal to
            array_instance = MyGate.Array(8)
        :return: gate array constructor function. or an gate array instance.
        """

        def select_register(port_type):
            """
            Select the register which will hold ports by the same type.
            """
            if issubclass(port_type, std_logic.In):
                return std_logic.InputRegister
            if issubclass(port_type, std_logic.Out):
                return std_logic.OutputRegister

        class _GateArray(SimpleArray):
            """
            This is array which represents the gate array.
            """

            @auto_synthesis
            def __init__(self, size):
                super(_GateArray, self).__init__(size, cls, auto_synthesis=False,
                                                 *map(select_register, cls.ports_signature()))

        # Give the newly generated class a proper name according to the class which created it.
        _GateArray.__name__ = cls.__name__ + "Array"
        if size:
            return _GateArray(size)
        return _GateArray
