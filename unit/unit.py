import command_shell


class Unit(object):
    def __init__(self, blockspace):
        self.blockspace = blockspace
        self.compounds = dict()

    def shell(self, item):
        return command_shell.shell_factory(item, self.blockspace)