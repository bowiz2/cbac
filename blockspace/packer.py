from compound import CBA
from constants import direction
from constants.block_id import ISOLATORS
from utils import Location
from collections import namedtuple
from utils import Vector, memoize


BlockAssignment = namedtuple('BlockAssignment', ['block', 'location', 'direction'])


class PackingError(BaseException):
    """
    Thrown when the block space cannot assign coordinates for a compound in a specific location.
    """
    pass


class Area(object):
    # The direction from which the build starts.
    start_build_direction = direction.WEST

    def __init__(self, compound):
        self._compound = compound
        self.packed_blocks = self._pack(compound)

    @property
    def compound(self):
        return self._compound

    @compound.setter
    def compound(self, value):
        self._compound = value
        self.packed_blocks = self._pack(value)

    @staticmethod
    def _pack(compound):
        """
        :return: list of relative Block Assignments.
        """
        # The corner of the area, the build starts from here.
        corner = Vector(0, 0, 0)

        build_direction = Area.start_build_direction

        packed = []

        for i, block in enumerate(compound.blocks):
            build_direction_vector = direction.vectors[build_direction]
            relative_location = corner + (build_direction_vector * i)
            relative_assignment = BlockAssignment(block, relative_location, build_direction)
            packed.append(relative_assignment)

        return packed

    @property
    def dimensions(self):
        """
        :return: Get the width, height and length of the area.
        """

        max_x = 0
        max_y = 0
        max_z = 0

        for block, rel_locatiom, direction in self.packed_blocks:
            if rel_locatiom[0] > max_x:
                max_x = rel_locatiom[0]
            if rel_locatiom[1] > max_y:
                max_y = rel_locatiom[1]
            if rel_locatiom[2] > max_z:
                max_z = rel_locatiom[2]

        return Vector(max_x, max_y, max_z)


class DummyArea(Area):
    """
    Used for tests
    """
    def __init__(self):
        self.compound = None
        self.packed_blocks = None


def pack(compounds, blockspace):
    """
    Takes a collection of compounds and packs them into the blockspace.
    :param compounds:
    :param blockspace:
    :return: list of block assignments.
    """
    areas = [Area(compound) for compound in compounds]
    area_assignments = pack_areas(areas, blockspace)

    block_assignments = []

    for area, area_location in area_assignments.items():
        for block, block_relative_location, block_direction in area.packed_blocks:
            assignment = BlockAssignment(block, area_location + block_relative_location, block_direction)
            block_assignments.append(assignment)

    return block_assignments



def pack_areas(areas, blockspace):
    """
    Takes a colelction of areas and organizes them inside the
    :param areas:
    :param blockspace:
    :return: dictionery of area and the location inside the blockspace.
    """
    pass