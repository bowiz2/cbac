from constants import direction
from constants.block_id import ISOLATORS
from utils import Vector, Location
import packer


DEF_BUILD_DIRECTION = direction.WEST


class BlockSpace(object):
    """
    Logical representation of blocks in the world
    """

    def __init__(self, size):
        # Tuple which describes the size of the block space (x,y,z)
        self.size = size
        self.packed_compounds = {}
        self.packed_entities = {}

        # Saves the locations of the isolated objects
        self._isolated_blocks_locations = []
        # Saves the locations of the compounds.

        # List of units in this blockspace.
        self.unpacked_compounds = []
        # Saves the locations of the entities.

        # holds to which side each block is faced to.

    def add_unit(self, unit):
        """
        takes a unit and tries to place it in the blockspace.
        :param unit: dict of compounds and relative poistion
        """
        for compound in unit.compounds:
            self.add_compound(compound)

        for other_unit in unit.dependent_units:
            self.add_unit(other_unit)

    def add_compound(self, compound):
        """
        Schedule the compound for mapping.
        """
        if compound in self.unpacked_compounds:
            return
        self.unpacked_compounds.append(compound)

    def add_entity(self, entity, location=(0, 0, 0)):
        """
        Add entity to the blockspace.
        """
        location = Vector(*location)
        self.packed_entities[entity] = location

    # Checkers
    def is_location_out_of_bounds(self, location):
        """
        Check if a location is not outside of the bounds of this block-space.
        """
        for location_d, size_d in zip(location, self.size):
            if location_d < 0:
                return True
            if location_d > size_d - 1:
                return True

    def is_isolated(self, location):
        """
        Check if a location is isolated from other redstone sources.
        """
        # TODO: Optimize and make smarter.
        # Generate a list of locations which are adjacent to the tested location.
        adjacent_locations = [location + vector for vector in direction.vectors.values()]

        # iterate over all the blocks in the blockspace and see if they are adjacent to the location.
        for block, block_location in self.packed_blocks.items():
            if block_location in adjacent_locations:
                if block.block_id not in ISOLATORS:
                    return False

        return True

    # Getters
    def get_area_of(self, item):
        """
        Gets the area of a compound.
        """

        if item in self.packed_compounds:
            location, block_packings = self.packed_compounds[item]
            # TODO: fix
            block_locations = [self.packed_blocks[block] for block, location, direction in block_packings]

            # TODO: remove code duplication.
            min_x = sorted(block_locations, key=lambda item: item[0])[0].x
            min_y = sorted(block_locations, key=lambda item: item[1])[0].y
            min_z = sorted(block_locations, key=lambda item: item[2])[0].z

            max_x = sorted(block_locations, key=lambda item: item[0])[-1].x
            max_y = sorted(block_locations, key=lambda item: item[1])[-1].y
            max_z = sorted(block_locations, key=lambda item: item[2])[-1].z

            return Vector(min_x, min_y, min_z), Vector(max_x, max_y, max_z)
        else:
            location = self.packed_blocks[item]
            return location, location

    def get_location_of(self, item):
        """
        Get a location of an item which is stored in the block space.
        """
        # if item is a location, return itself.
        if isinstance(item, Vector):
            return item
        try:
            location = self.packed_blocks[item]
        except KeyError:
            location = self.packed_compounds[item].location

        return location

    def pack(self):
        compound_packings = packer.pack(self.unpacked_compounds)
        for compound, packing in compound_packings.items():
            self.packed_compounds[compound] = packing

    @property
    def packed_blocks(self):
        to_return = {}
        for compound in self.packed_compounds.values():
            for block, location, build_direction in compound.block_assignments:
                try:
                    block.facing = build_direction
                except AttributeError:
                    pass
                to_return[block] = location
        return to_return

    def shrink(self):
        """
        Shrinks the blockspace size to the minimal, according to its blocks.
        """
        # TODO: remove code duplication.
        block_locations = self.packed_blocks.values()
        max_x = sorted(block_locations, key=lambda item: item[0])[-1].x
        max_y = sorted(block_locations, key=lambda item: item[1])[-1].y
        max_z = sorted(block_locations, key=lambda item: item[2])[-1].z
        self.size = (max_x + 1, max_y + 1, max_z + 1)


