from unit import Unit


class TimerUnit(Unit):
    def __init__(self, count):
        super(TimerUnit, self).__init__(0)
        self.count = count
        self.generate_main_logic_cbas()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        for i in xrange(self.count):
            yield "/say {0}".format(i)
