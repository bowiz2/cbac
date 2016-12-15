"""
Holds area factory methods.
"""
from cbac.core.blockspace.area import LineArea, RawArea, BlockBoxArea, WindedArea
from pymclevel import MCSchematic

from cbac.core.blockbox import BlockBox
from cbac.core.compound import CommandBlockArray


def area_factory(obj):
    """
    Takes an object and construct an area object out of it.
    :return: Area
    """
    if isinstance(obj, MCSchematic):
        return RawArea(obj)

    if isinstance(obj, BlockBox):
        return BlockBoxArea(obj)

    if isinstance(obj, CommandBlockArray):
        return WindedArea(obj)

    return LineArea(obj)
