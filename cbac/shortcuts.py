import cbac

std_unit_gates = [cbac.std_unit.AndGate, cbac.std_unit.OrGate, cbac.std_unit.NandGate, cbac.std_unit.XorGate,
                  cbac.std_unit.XnorGate]

std_unit_arithmetics = [cbac.std_unit.RippleCarryFullAdderArray, cbac.std_unit.IncrementUnit, cbac.std_unit.NegateUnit,
                        cbac.std_unit.SubtractUnit, cbac.std_unit.MultiUnit]
