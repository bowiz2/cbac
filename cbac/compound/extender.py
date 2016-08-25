from cbac.command_shell import BlockShell
from cbac.compound import CBA


class Extender(CBA):
    """
    When you activate this CBA, it will activate all the targets.
    """

    def __init__(self, *targets):
        super(Extender, self).__init__(*[BlockShell(target.activator).activate() for target in targets])
