from cbac.compound import CBA
from cbac.unit.statements import MainLogicJump
from cbac.unit.unit_base import Unit


class CallbackUnit(Unit):
    def __init__(self, bits=8):
        super(CallbackUnit, self).__init__(bits)
        # == Here you declare all your memory slots.

        self.curse = self.add(CBA("/say 1", "/say 2", "/say 3", "/say callback"))
        self.a_callback = self.add(CBA("/say its the callback of a"))
        self.a = self.add(CBA(
            "/say a",
            self.curse.shell.set_callback(self.a_callback),
            self.curse.activator.shell.activate())
        )

        self.b_callback = self.add(CBA("/say its the callback of b"))
        self.b = self.add(CBA(
            "/say b",
            self.curse.shell.set_callback(self.b_callback),
            self.curse.activator.shell.activate())
        )

        # ==
        self.synthesis()

    def architecture(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield "/say main logic start"
        yield MainLogicJump(self.a)
        yield "/say main logic end"
