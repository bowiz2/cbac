import cbac

std_unit_gates = [cbac.std_unit.AndGate, cbac.std_unit.OrGate, cbac.std_unit.NandGate, cbac.std_unit.XorGate,
                  cbac.std_unit.XnorGate]

std_unit_arithmetics = [cbac.std_unit.RippleCarryFullAdderArray, cbac.std_unit.IncrementUnit, cbac.std_unit.NegateUnit,
                        cbac.std_unit.SubtractUnit, cbac.std_unit.MultiUnit]


class procedure:
    """
    Usage
    block_space.add(porcedure("simple_setup").body(
        say("helo"),
        other_command(),
    ))
    """

    # TODO: move procedure to better place.
    def __init__(self, name):
        self.name = name

    def body(self, *statements):
        from cbac.core.compound.cb_array import CommandBlockArray
        from cbac.core.mc_command import say
        return CommandBlockArray(say("Procedure: {0}".format(self.name)), *statements)


__all__ = ['std_unit_gates', 'std_unit_arithmetics', 'block_ids']
