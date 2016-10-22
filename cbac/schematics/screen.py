"""
Holds the Screen schematics
"""
from pymclevel import MCSchematic
from pkg_resources import resource_filename
from cbac.schematics.common import RESOURCE_MODULE

BLACK_SCREEN_128x128 = MCSchematic(filename=resource_filename(RESOURCE_MODULE, 'screen_128x128.schematic'))