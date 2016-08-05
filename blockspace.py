from utils import Vector, Location
from constants import direction
from constants.block_id import ISOLATORS
from unit import Unit

class BlockSpace(object):
    """
    Logical representation of blocks in the world
    """

    def __init__(self, size, *compounds):
        # Tuple which describes the size of the block space (x,y,z)
        self.size = size
        # Saves the locations of the blocks.
        self.blocks = dict()
        # Saves the locations of the isolated objects
        self._isolated_blocks_locations = list()
        # Saves the locations of the compounds.
        self.compounds = dict()
        # Saves the locations of the entities.
        self.entities = dict()
        # holds to which side each block is faced to.

        for compound in compounds:
            self.add_compound(compound)

    def add_unit(self, unit):
        """
        takes a unit and tries to place it in the blockspace.
        :param unit: dict of compounds and relative poistion
        """
        # TODO: cleanup mess.
        if isinstance(unit, dict):
            compounds_dict = unit
        elif isinstance(unit, Unit):
            compounds_dict = unit.compounds
        else:
            raise Exception("Unit is of an unknown type.")

        for unit_location in self.possible_locations_for(unit):
            try:
                compound_assigments = {compound: dict(self.assign_coordinates(unit_location + compound_location, compound)) for compound, compound_location in compounds_dict.items()}
                for compound, assigments in compound_assigments.items():
                    self.add_blocks(assigments, compound.isolated)
                    self.compounds[compound] = unit_location + compounds_dict[compound], assigments
                return

            except AssignmentError:
                pass

        raise Exception("Cant add unit.")

    def add_compound(self, compound, location=None, build_direction=direction.NORTH):
        """
        Mainly, Generate the blocks of that compound to the block dict.
        """
        # Generates possible locations for the new compound.
        if location is None:
            possible_locations = self.possible_locations_for(compound)
        else:
            # The user can force the blockspace to use a specific location.
            possible_locations = [location]

        for location in possible_locations:
            try:
                # Generate assignments.
                assignments = dict(self.assign_coordinates(location, compound, build_direction))
                self.add_blocks(assignments, build_direction)
                # Save the compound location.
                self.compounds[compound] = (location, assignments)
                return
            except AssignmentError:
                # Means the the assignment for this generation is not possible.
                pass
        raise Exception("Can't add compound {0} to this block space.".format(compound))

    def add_blocks(self, blocks, isolated=False, build_direction=None):
        for block, coordinate in blocks.items():
            # TODO: think if it is good for here.
            try:
                if block.facing is None:
                    block.facing = direction.oposite(build_direction)
            except AttributeError:
                pass
            self.blocks[block] = coordinate
            if isolated:
                self._isolated_blocks_locations.append(coordinate)

    def add_entity(self, entity, location=(0, 0, 0)):
        """
        Add entity to the blockspace.
        """
        location = Vector(*location)
        self.entities[entity] = location

    def is_location_out_of_bounds(self, location):
        """
        Check if a location is not outside of the bounds of this block-space.
        """
        for location_d, size_d in zip(location, self.size):
            if location_d < 0:
                return True
            if location_d > size_d - 1:
                return True

    def possible_locations_for(self, obj):
        """
        Generate possible location in which a compound can stand at.
        """
        for x in xrange(self.size[0]):
            for y in xrange(self.size[1]):
                for z in xrange(self.size[2]):
                    yield Location(x, y, z)

        raise AssignmentError("Can't find location for compound {0}.".format(obj))

    def assign_coordinates(self, location, compound, build_direction):
        """
        For each block in the compound, assign a coordinate for it.
        """
        # For each block try to assign location and hope for the location to match.
        for i, block in enumerate(compound.blocks):

            # try to assign location.
            direction_vector = direction.vectors[build_direction]

            possible_location = location + (direction_vector * i)

            if possible_location in self.blocks.values():
                raise AssignmentError("Collision with block at location {0}".format(possible_location))

            if self.is_location_out_of_bounds(possible_location):
                raise AssignmentError("Location out of bounds.")

            if compound.isolated and not self.is_isolated(possible_location):
                raise AssignmentError("Location not isolated while isolation is required.")

            if block.block_id not in ISOLATORS:
                for isolated_location in self._isolated_blocks_locations:
                    if isolated_location.is_adjacent(possible_location):
                        raise AssignmentError("Location interferes with the isolation of other compounds.")

            assigned_location = possible_location

            yield block, assigned_location

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

    def get_area_of(self, compound):
        """
        Gets the area of a compound.
        """
        location, blocks = self.compounds[compound]
        block_locations = [self.blocks[block] for block in blocks]
        # TODO: remove code duplication.
        min_x = sorted(block_locations, key=lambda item: item[0])[0].x
        min_y = sorted(block_locations, key=lambda item: item[1])[0].y
        min_z = sorted(block_locations, key=lambda item: item[2])[0].z

        max_x = sorted(block_locations, key=lambda item: item[0])[-1].x
        max_y = sorted(block_locations, key=lambda item: item[1])[-1].y
        max_z = sorted(block_locations, key=lambda item: item[2])[-1].z

        return Vector(min_x, min_y, min_z), Vector(max_x, max_y, max_z)

    def get_location_of(self, item):
        """
        Get a location of an item which is stored in the block space.
        """
        try:
            location = self.blocks[item]
        except KeyError:
            location, blocks = self.compounds[item]

        return location


class AssignmentError(BaseException):
    """
    Thrown when the block space cannot assign coordinates for a compound in a specific location.
    """
    pass
