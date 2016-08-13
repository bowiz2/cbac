from unit import Unit
from compound import CBA


class CallbackUnit(Unit):
    def __init__(self, bits=8):
        super(CallbackUnit, self).__init__(bits)
        # == Here you declare all your memory slots.

        self.curse = self.add_compound(CBA("/say 1", "/say 2", "/say 3", "/say callback"))
        self.a = self.add_compound(CBA(
            "/say a",
            self.curse.blocks[4].shell.change_command("/say callbacking to a"),
            self.curse.activator.shell.activate())
        )
        self.b = self.add_compound(CBA(
            "/say b",
            self.curse.blocks[4].shell.change_command("/say callbacking to b"),
            self.curse.activator.shell.activate())
        )

        # ==
        self.generate_main_point_entry()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield "/say a"
