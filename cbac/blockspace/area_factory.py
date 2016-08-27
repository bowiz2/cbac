from pymclevel import MCSchematic
from .area import Area, RawArea


def area_factory(obj):
    """
    Takes an object and construct an area object out of it.
    :return: Area
    """
    if isinstance(obj, MCSchematic):
        return RawArea(obj)
    if isinstance(obj, BlockBox):
        return BlocBoxArea(obj)
    return Area(obj)
