from compound import CBA
from constants import direction
from constants.block_id import ISOLATORS
from utils import Location
from collections import namedtuple

BlockAssignment = namedtuple('BlockAssignment', ['location', 'direction'])


class PackingError(BaseException):
    """
    Thrown when the block space cannot assign coordinates for a compound in a specific location.
    """
    pass

class Area(object):
    def __init__(self, compound):
        self.compound = compound

    def pack(self):
        """
        :return: list of relative Block Assignments.
        """
        pass

    def get_dimensions(self):
        """
        :return: Get the width, height and length of the area.
        """
        pass

def pack(compounds, blockspace):
    """
    Takes a collection of compounds and packs them into the blockspace.
    :param compounds:
    :param blockspace:
    :return: list of block assignments.
    """
    areas = [Area(compound) for compound in compounds]
    area_assignments = pack_areas(areas, blockspace)

    block_assignments = {}
    for area, location in area_assignments.items():
        for block_location, block_direction in area.pack():
            


def pack_areas(areas, blockspace):
    """
    Takes a colelction of areas and organizes them inside the
    :param areas:
    :param blockspace:
    :return: dictionery of area and the location inside the blockspace.
    """
    pass