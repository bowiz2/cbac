from compound import CBA
from unit import Unit, MainLogicJump


class CallbackUnit(Unit):
    def __init__(self, bits=8):
        super(CallbackUnit, self).__init__(bits)
        # == Here you declare all your memory slots.

        self.curse = self.add_compound(CBA("/say 1", "/say 2", "/say 3", "/say callback"))
        self.a_callback = self.add_compound(CBA("/say its the callback of a"))
        self.a = self.add_compound(CBA(
            "/say a",
            self.curse.shell.set_callback(self.a_callback),
            self.curse.activator.shell.activate())
        )

        self.b_callback = self.add_compound(CBA("/say its the callback of b"))
        self.b = self.add_compound(CBA(
            "/say b",
            self.curse.shell.set_callback(self.b_callback),
            self.curse.activator.shell.activate())
        )

        # ==
        self.generate_main_logic_cbas()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield "/say main logic start"
        yield MainLogicJump(self.a)
        yield "/say main logic end"