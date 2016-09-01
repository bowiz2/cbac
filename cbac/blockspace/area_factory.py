"""
Holds area factory methods.
"""
from cbac.blockbox import BlockBox
from cbac.compound import CBA
from pymclevel import MCSchematic

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

    return LineArea(obj)
