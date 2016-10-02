import cbac.constants.entity_id
from cbac import Entity


class Pivot(Entity):
    """
    An armor stand which can move in space and copy areas
    """
    def __init__(self, area_of_affect=((0, 0, 0), (1, 1, 1)), invisible=False):
        """
        :param area_of_affect: This is the area which is copied to and from the pivot.
        """
        tags = {"Invisible": 1} if invisible else {}
        super(Pivot, self).__init__(cbac.constants.entity_id.ARMOR_STAND, no_gravity=True, tags=tags)
        self.area_of_affect = area_of_affect
