import cbac
from cbac.core.constants import block_id as block_ids


std_unit_gates = [cbac.std_unit.AndGate, cbac.std_unit.OrGate, cbac.std_unit.NandGate, cbac.std_unit.XorGate,
                  cbac.std_unit.XnorGate]

std_unit_arithmetics = [cbac.std_unit.RippleCarryFullAdderArray, cbac.std_unit.IncrementUnit, cbac.std_unit.NegateUnit,
                        cbac.std_unit.SubtractUnit, cbac.std_unit.MultiUnit]


class procedure:
    def __init__(self, name):
        self.name = name

    def body(self):
        from cbac.core.compound.cba import CBA
        from cbac.core.mc_command import say
        return CBA(say("Procedure: ".format(self.name)))

__all__ = ['std_unit_gates', 'std_unit_arithmetics', 'block_ids']