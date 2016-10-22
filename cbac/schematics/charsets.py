"""
Holds all the char set schematics.
"""
import pymclevel
from pkg_resources import resource_filename
from cbac.schematics.common import RESOURCE_MODULE

AZ_CAPS = pymclevel.MCSchematic(filename=resource_filename(RESOURCE_MODULE, 'az_caps.schematic'))
AZ_CAPS_COMPRESSED = pymclevel.MCSchematic(filename=resource_filename(RESOURCE_MODULE, 'az_caps_compressed.schematic'))
ASCII = pymclevel.MCSchematic(filename=resource_filename(RESOURCE_MODULE, 'ascii.schematic'))
