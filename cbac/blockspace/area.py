import utils

from .assignment import BlockAssignment
from cbac.block import Block
from constants import mc_direction
from utils import Vector


class Area(object):
    def __init__(self, wrapped_item, start_build_direction=mc_direction.EAST):
        self.wrapped = wrapped_item
        self.start_build_direction = start_build_direction

    def _pack(self, compound):
        corner = Vector(0, 0, 0)
        build_direction = self.start_build_direction

        packed = []

        for i, block in enumerate(compound.blocks):
            build_direction_vector = utils.vectors[build_direction]
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
        packed_blocks = self._pack(self.wrapped)
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
        return self.wrapped.isolated

# class LineArea(Area):
#     """
#     An area which constructs a line out of blocks.
#     """
#     pass
#     # TODO: implement.


class WindedArea(Area):
    """
    An area which was winded from a long line of blocks into a compressed block area.
    """
    def __init__(self, wrapped_item, max_width=8):
        super(WindedArea, self).__init__(wrapped_item)
        self.max_width = max_width

    def _pack(self, compound):
        # TODO: document
        build_direction = self.start_build_direction
        # Matrix of rows.
        rows = []
        row = []
        # All the blocks of the compound.
        total_blocks = compound.blocks
        # Generate rows from blocks.
        for i, block in enumerate(total_blocks):
            row.append(block)
            if i % self.max_width is self.max_width - 1:
                rows.append(row)
                row = []

        rows.append(row)
        last_row = rows[-1]
        for i in xrange(self.max_width - len(last_row)):
            # Append none for operation
            last_row.append(None)
        directions = {}
        locs = {}
        # set directions for the blocks.
        for row_id, row in enumerate(rows):
            for block_id, block in enumerate(row):
                if block_id % self.max_width is not self.max_width -1:
                    directions[block] = [build_direction, mc_direction.oposite(build_direction)][row_id % 2]
                else:
                    directions[block] = mc_direction.UP
            if row_id % 2 is 1:
                row.reverse()
        # set locations for the blocks.
        for row_id, row in enumerate(rows):
            for block_id, block in enumerate(row):
                locs[block] = Vector(block_id, row_id, 0)
        # compile assignments
        return [BlockAssignment(block, locs[block], directions[block]) for block in total_blocks]


class RawArea(Area):
    """
    An area which was constructed from a schematic file.
    """
    def __init__(self, schematic):
        self.schematic = schematic

    @property
    def packed_blocks(self):
        to_return = []
        for x, block_plane in enumerate(self.schematic.Blocks):
            for y, block_row in enumerate(block_plane):
                for z, block_id in enumerate(block_row):
                    to_return.append(BlockAssignment(Block(block_id), Vector(x, y, z), None))
        return to_return