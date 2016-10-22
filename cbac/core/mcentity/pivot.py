import cbac.core.constants.entity_id
from cbac.core.command_shell.entity_shell import PivotShell

from cbac.core.mcentity import MCEntity
from cbac.core.utils import memoize


class Pivot(MCEntity):
    """
    An armor stand which can move in space and copy areas
    """

    def __init__(self, invisible=False):
        """
        :param area_of_affect: This is the area which is copied to and from the pivot.
        """
        tags = {"Invisible": 1} if invisible else {}
        super(Pivot, self).__init__(cbac.core.constants.entity_id.ARMOR_STAND, no_gravity=True, tags=tags)

    @property
    @memoize
    def shell(self):
        return PivotShell(self)
