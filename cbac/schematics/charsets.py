"""
Holds all the char set schematics.
"""
from pymclevel import MCSchematic
from pkg_resources import resource_filename
from cbac.schematics.common import SCHEMATIC_RESOURCES_MODULE


AZ_CAPS = MCSchematic(filename=resource_filename(SCHEMATIC_RESOURCES_MODULE, 'az_caps.schematic'))
AZ_CAPS_COMPRESSED = MCSchematic(filename=resource_filename(SCHEMATIC_RESOURCES_MODULE, 'az_caps_compressed.schematic'))
ASCII = MCSchematic(filename=resource_filename(SCHEMATIC_RESOURCES_MODULE, 'ascii.schematic'))