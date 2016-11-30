import cbac
import cpu8051
from cbac.unit.statements import If
from cbac.core import mc_command


class Handler(cbac.unit.Unit):
    """
    Handles a specific opcode in the cpu.
    """
    opcode_set = None  # type: cpu8051.opcode.OpcodeSet

    @cbac.unit.auto_synthesis
    def __init__(self, cpu_body, debug=False):
        super(Handler, self).__init__(bits=cpu_body.bits)
        assert isinstance(cpu_body, cpu8051.body.Cpu8051)
        self.cpu = cpu_body
        self._debug = debug

    def get_register(self, value):
        """
        :return: get the register encoded in the opcode.
        """
        assert self.opcode_set, "must have opcode set."
        return self.cpu.general_registers[self.opcode_set.get_arg(value, 'r')]

    def handle(self, opcode_value=None):
        """
        This architecture will be generated for each opcode in the opcode set.
        :param opcode_value: Here will be passed the currently generated opcode. can be ignored if opcode set size is 1.
        :return: Generator which is an architecture which describes how to behave depending on the opcode.
        """
        yield None

    def architecture(self):
        if self._debug:
            yield mc_command.say("{} entry".format(self.__class__.__name__))

        for opcode in self.opcode_set.all():
            yield If(self.cpu.opcode_is(opcode)).then(
                *list(self.handle(opcode))
            )
