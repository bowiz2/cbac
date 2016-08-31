from cbac.blockbox import BlockBox
from pymclevel import MCSchematic
from cbac.compound import CBA

from .area import LineArea, RawArea, BlockBoxArea, WindedArea


def area_factory(obj):
    """
    Takes an object and construct an area object out of it.
    :return: Area
    """
    if isinstance(obj, MCSchematic):
        return RawArea(obj)

    if isinstance(obj, BlockBox):
        return BlockBoxArea(obj)

    if isinstance(obj, CBA):
        return WindedArea(obj)

    return LineArea(obj)
