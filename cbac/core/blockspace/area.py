"""
Declarations of objects which are wrapping items to be packed into a blockspace.
"""
from cbac.core.block import Block
from cbac.core.blockspace.assignment import BlockAssignment
from cbac.core.blockspace.winder import winde
from cbac.core.mc_direction import MCDirection

from cbac.core.utils import Vector


# TODO: test raw area.
# TODO: rename winded area.


class Area(object):
    """
    Wraps an object for packing.
    """

    def __init__(self, wrapped_item):
        self.wrapped = wrapped_item

    def _assign(self, obj):
        """
        Create a block assignment for each block representation in obj.
        Must be implemented.
        :param obj: holds representation for blocks.
        :return: list of block assignments.
        """
        return []

    @property
    def packed_blocks(self):
        """
        :return: list of relative Block Assignments.
        """
        # The corner of the area, the build starts from here.
        packed_blocks = self._assign(self.wrapped)
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


class LineArea(Area):
    """
    An area which constructs a line out of blocks.
    """

    def __init__(self, compound, start_build_direction=MCDirection.EAST):
        super(LineArea, self).__init__(compound)
        self.start_build_direction = start_build_direction

    def _assign(self, compound):
        corner = Vector(0, 0, 0)
        build_direction = self.start_build_direction

        packed = []

        for i, block in enumerate(compound.blocks):
            build_direction_vector = MCDirection.vectors[build_direction]
            relative_location = corner + (build_direction_vector * i)
            relative_assignment = BlockAssignment(block, relative_location, build_direction)
            packed.append(relative_assignment)

        return packed


class WindedArea(LineArea):
    """
    An area which was winded from a long line of blocks into a compressed block area.
    """

    def __init__(self, wrapped_item, max_width=8):
        super(WindedArea, self).__init__(wrapped_item)
        self.max_width = max_width

    def _assign(self, compound):
        """
        Takes a compound a compresses it to the maximum width. It is actually winding the row. Used mainly for CBAs.
        :param compound: a cba you want ot compress.
        :return:
        :note: That this does not account for conditional commands.
        """
        return winde(list(compound.blocks), self.max_width, self.start_build_direction)


class BlockBoxArea(Area):
    """
    An area of a block box.
    """

    @property
    def block_box(self):
        """
        :return: wrapped block box.
        """
        return self.wrapped

    @property
    def packed_blocks(self):
        """
        :return: A list of relatively packed blocks.
        """
        to_return = []
        for x, block_plane in enumerate(self.block_box.blocks):
            for y, block_row in enumerate(block_plane):
                for z, block_id in enumerate(block_row):
                    to_return.append(BlockAssignment(self.block_box[x][y][z], Vector(z, y, x), None))
        return to_return


class RawArea(Area):
    """
    An area which was constructed from a schematic file.
    DONT USE, DEPRECATED>
    """

    def __init__(self, schematic):
        super(RawArea, self).__init__(schematic)

    @property
    def schematic(self):
        """
        :return: Wrapped schematic.
        """
        return self.wrapped

    @property
    def packed_blocks(self):
        """
        :return: List of relatively packed blocks.
        """
        to_return = []
        for x, block_plane in enumerate(self.schematic.Blocks):
            for z, block_row in enumerate(block_plane):
                for y, block_id in enumerate(block_row):
                    to_return.append(
                        BlockAssignment(Block(block_id, block_data=self.schematic.Data[x][z][y]), Vector(x, y, z),
                                        None))
        return to_return

    @property
    def is_isolated(self):
        return False


__all__ = ["LineArea", "WindedArea", "BlockBoxArea", "RawArea"]
