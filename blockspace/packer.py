from collections import namedtuple, defaultdict
from compound import CBA
from constants import direction
from utils import Vector

BlockAssignment = namedtuple('BlockAssignment', ['block', 'location', 'direction'])
CompoundAssignment = namedtuple('CompoundAssignment', ['location', 'block_assignments'])

class PackingError(BaseException):
    """
    Thrown when the block space cannot assign coordinates for a compound in a specific location.
    """
    pass

# The direction from which the build starts.
start_build_direction = direction.EAST


class Area(object):
    def __init__(self, compound):
        self.compound = compound

    @staticmethod
    def _pack(compound):
        corner = Vector(0, 0, 0)
        build_direction =  start_build_direction

        packed = []

        for i, block in enumerate(compound.blocks):
            build_direction_vector = direction.vectors[build_direction]
            relative_location = corner + (build_direction_vector * i)
            relative_assignment = BlockAssignment(block, relative_location, build_direction)
            packed.append(relative_assignment)

        return packed

    @property
    def packed_blocks(self):
        """
        :return: list of relative Block Assignments.
        """
        # The corner of the area, the build starts from here.
        packed_blocks = self._pack(self.compound)
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

        return result

    @property
    def is_isolated(self):
        """
        Returns if the area must be isolated.
        :return: boolean
        """
        return self.compound.isolated

max_width = 8

class CBAArea(Area):
    @staticmethod
    def _pack(compound):
        # TODO: document
        build_direction = start_build_direction

        rows = []
        row = []
        total_blocks = compound.blocks
        for i, block in enumerate(total_blocks):
            row.append(block)
            if i % max_width is max_width -1 :
                rows.append(row)
                row = []
                row_id = []
        rows.append(row)
        last_row = rows[-1]
        for i in xrange(max_width - len(last_row)):
            #Append none for operation
            last_row.append(None)
        directions = {}
        locs = {}
        # set directions for the blocks.
        for row_id, row in enumerate(rows):
            for block_id, block in enumerate(row):
                if block_id % max_width is not max_width -1:
                    directions[block] = [build_direction, direction.oposite(build_direction)][row_id % 2]
                else:
                    directions[block] = direction.UP
            if row_id % 2 is 1:
                row.reverse()
        # set locations for the blocks.
        for row_id, row in enumerate(rows):
            for block_id, block in enumerate(row):
                locs[block] = Vector(block_id, row_id, 0)
        # compile assignments
        return [BlockAssignment(block, locs[block], directions[block]) for block in total_blocks]

def area_factory(compound):
    if isinstance(compound, CBA):
        return CBAArea(compound)
    else:
        return Area(compound)

def pack(compounds):
    """
    Takes a collection of compounds and packs them into the blockspace.
    :param compounds:
    :param blockspace:
    :return: list of block assignments.
    """
    areas = [area_factory(compound) for compound in compounds]

    area_assignments = pack_areas(areas)

    compound_packings = {}

    for area, area_location in area_assignments.items():
        compound_assignment = CompoundAssignment(
            location=area_location,
            block_assignments=[BlockAssignment(block, area_location + relative_block_location, block_direction)
                               for block, relative_block_location, block_direction in area.packed_blocks]
        )

        compound_packings[area.compound] = compound_assignment

    return compound_packings


def pack_areas(areas):
    """
    Takes a colelction of areas and organizes them inside the
    :param areas:
    :param blockspace:
    :return: dictionery of area and the location inside the blockspace.
    """
    assignments = {}
    pivot = Vector(0, 0, 0)
    # TODO: adjust to build direction
    for area in areas:
        assignments[area] = pivot
        if area.is_isolated:
            pivot += Vector(0, 0, 2)
        pivot += Vector(0, 0, area.dimensions.z)

    return assignments


