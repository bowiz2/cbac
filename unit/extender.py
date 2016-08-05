from compound import CBA
from unit import Unit


class Extender(Unit):
    def __init__(self, blockspace, *targets):
        super(Extender, self).__init__(blockspace)
        commands = []
        for target in targets:
            commands.append(self.shell(target.activator).activate())
        self.cba = CBA(*commands)
        self.compounds[self.cba] = (0, 0, 0)
