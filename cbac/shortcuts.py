from cbac import std_unit

std_unit_gates = [std_unit.AndGate, std_unit.OrGate, std_unit.NandGate, std_unit.XorGate, std_unit.XnorGate]
std_unit_arithmetics = [std_unit.RippleCarryFullAdderArray, std_unit.IncrementUnit, std_unit.NegateUnit,
                        std_unit.SubtractUnit, std_unit, std_unit.MultiUnit]
