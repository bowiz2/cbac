import cbac.constants.entity_id
from cbac import Entity
from cbac.utils import memoize
from cbac.command_shell.entity_shell import PivotShell


class Pivot(Entity):
    """
    An armor stand which can move in space and copy areas
    """
    def __init__(self, invisible=False):
        """
        :param area_of_affect: This is the area which is copied to and from the pivot.
        """
        tags = {"Invisible": 1} if invisible else {}
        super(Pivot, self).__init__(cbac.constants.entity_id.ARMOR_STAND, no_gravity=True, tags=tags)

    @property
    @memoize
    def shell(self):
        # TODO: convert each shell property to class method.
        return PivotShell(self)
