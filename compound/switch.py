from compound.cba import CBA


class SwitchFlow(CBA):
    """
    Switches to a case given an item.
    """

    def __init__(self, item, cases):
        commands = list()
        self.comparables = list()
        for value, target in cases.items():
            commands.append(item.shell == value)
            try:
                commands.append(target.activator.shell.activate())
            except AttributeError:
                commands.append(target)
            self.comparables.append(value)
        super(SwitchFlow, self).__init__(*commands)