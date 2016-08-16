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
        # Saves the locations of the blocks.
        self.blocks = {}
        self.directions = {}
        # Saves the locations of the isolated objects
        self._isolated_blocks_locations = list()
        # Saves the locations of the compounds.
        self.compounds = dict()
        # List of units in this blockspace.
        self.units = []
        # Saves the locations of the entities.
        self.entities = dict()
        # holds to which side each block is faced to.

    def add_unit(self, unit, build_direction=DEF_BUILD_DIRECTION):
        """
        takes a unit and tries to place it in the blockspace.
        :param unit: dict of compounds and relative poistion
        """
        if unit in self.units:
            return
        for compound in unit.compounds:
            self.add_compound(compound, build_direction=build_direction)

        for other_unit in unit.dependent_units:
            self.add_unit(other_unit, build_direction=build_direction)

    def add_compound(self, compound, location=None, build_direction=DEF_BUILD_DIRECTION):
        """
        Mainly, Generate the blocks of that compound to the block dict.
        """
        if compound in self.compounds:
            return
        try:
            assignments = packer.pack(compound, self, location, build_direction)
            self.add_blocks(assignments)
            # Save the compound location.
            # TODO: fix location to the assigned location.
            self.compounds[compound] = (location, assignments)
        except packer.PackingError:
            raise Exception("Can't add compound {0} to this block space.".format(compound))

    def add_compounds(self, compounds, build_direction=DEF_BUILD_DIRECTION):
        for compound in compounds:
            self.add_compound(compound, None, build_direction=build_direction)

    def add_blocks(self, blocks, isolated=False):
        """
        Add blocks to the block sapce as long as they are not already in it.
        :param blocks: iterator over blocks to add to the blockspace.
        :param isolated: if you want the blocks to be isolated.
        :param build_direction: the direction you want to build the blocks to, if they have the facing option.
        :return:
        """
        for block,  pack_info in blocks.items():
            coordinate, pack_direction = pack_info
            if block not in self.blocks:
                # TODO: think if it is good for here.
                try:
                    if block.facing is None:
                        block.facing = direction.oposite(pack_direction)
                except AttributeError:
                    pass
                self.blocks[block] = coordinate
                self.directions[block] = pack_direction
                if isolated:
                    self._isolated_blocks_locations.append(coordinate)

                block._belongs_to_blockspace = True

    def add_entity(self, entity, location=(0, 0, 0)):
        """
        Add entity to the blockspace.
        """
        location = Vector(*location)
        self.entities[entity] = location

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
        for block, block_location in self.blocks.items():
            if block_location in adjacent_locations:
                if block.block_id not in ISOLATORS:
                    return False

        return True

    # Getters
    def get_area_of(self, item):
        """
        Gets the area of a compound.
        """

        if item in self.compounds:
            location, blocks = self.compounds[item]
            block_locations = [self.blocks[block] for block in blocks]

            # TODO: remove code duplication.
            min_x = sorted(block_locations, key=lambda item: item[0])[0].x
            min_y = sorted(block_locations, key=lambda item: item[1])[0].y
            min_z = sorted(block_locations, key=lambda item: item[2])[0].z

            max_x = sorted(block_locations, key=lambda item: item[0])[-1].x
            max_y = sorted(block_locations, key=lambda item: item[1])[-1].y
            max_z = sorted(block_locations, key=lambda item: item[2])[-1].z

            return Vector(min_x, min_y, min_z), Vector(max_x, max_y, max_z)
        else:
            location = self.blocks[item]
            return location, location

    def get_location_of(self, item):
        """
        Get a location of an item which is stored in the block space.
        """
        try:
            location = self.blocks[item]
        except KeyError:
            location, blocks = self.compounds[item]

        return location

    def shrink(self):
        """
        Shrinks the blockspace size to the minimal, according to its blocks.
        """
        # TODO: remove code duplication.
        block_locations = self.blocks.values()
        max_x = sorted(block_locations, key=lambda item: item[0])[-1].x
        max_y = sorted(block_locations, key=lambda item: item[1])[-1].y
        max_z = sorted(block_locations, key=lambda item: item[2])[-1].z
        self.size = (max_x + 1, max_y + 1, max_z + 1)


