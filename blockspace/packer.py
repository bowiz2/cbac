from collections import namedtuple

from constants import direction
from utils import Vector

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
        self.compound = compound

    def _pack(self, compound):
        corner = Vector(0, 0, 0)
        build_direction = self.start_build_direction

        packed = []

        for i, block in enumerate(compound.blocks):
            build_direction_vector = direction.vectors[build_direction]
            relative_location = corner + (build_direction_vector * i)
            relative_assignment = BlockAssignment(block, relative_location, build_direction)
            packed.append(relative_assignment)

        return packed

    @property
    def margin(self):
        if not self.compound.isolated:
            return Vector(0, 0, 0)
        else:
            return Vector(1, 1, 1)

    @property
    def packed_blocks(self):
        """
        :return: list of relative Block Assignments.
        """
        # The corner of the area, the build starts from here.
        packed_blocks = self._pack(self.compound)
        packed_blocks = [BlockAssignment(block, self.margin + location, direction) for block, location, direction in
                         packed_blocks]
        return packed_blocks

    @property
    def dimensions(self):
        """
        :return: Get the width, height and length of the area.
        """

        max_x = 0
        max_y = 0
        max_z = 0

        for block, rel_location, _ in self.packed_blocks:
            if rel_location[0] > max_x:
                max_x = rel_location[0]
            if rel_location[1] > max_y:
                max_y = rel_location[1]
            if rel_location[2] > max_z:
                max_z = rel_location[2]

        result = Vector(max_x, max_y, max_z)
        # Adjust for margin
        result += self.margin

        return result


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
