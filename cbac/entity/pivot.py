import cbac.constants.entity_id
from cbac import Entity


class Pivot(Entity):
    """
    An armor stand which can move in space and copy areas
    """
    def __init__(self, area_of_effect):
        """
        :param area_of_effect: This is the area which is copied to and from the pivot.
        """
        super(Pivot, self).__init__(cbac.constants.entity_id.ARMOR_STAND, custom_name="RAM_PIVOT", no_gravity=True)
        self.area_of_effect = area_of_effect