from utils import Vector, Location
from constants import direction


class BlockSpace(object):
    """
    Logical representation of blocks in the world
    """
    def __init__(self, size, *compounds):
        # Tuple which describes the size of the block space (x,y,z)
        self.size = size
        # Saves the locations of the blocks.
        self.blocks = dict()
        # Saves the locations of the compounds.
        self.compounds = dict()

        for compound in compounds:
            self.add_compound(compound)

    def add_compound(self, compound):
        """
        Mainly, Generate the blocks of that compound to the block dict.
        """
        # Generates possible locations for the new compound.
        possible_locations = self.possible_locations_for(compound)

        is_compound_added = False

        while not is_compound_added:
            try:
                # Get the next possible location.
                location = possible_locations.next()
                # Generate assignments.
                assignments = dict(self.assign_coordinates(location, compound))

                for block, coordinate in assignments.items():
                    self.blocks[block] = coordinate
                # Save the compound location.
                self.compounds[compound] = (location, assignments)
                is_compound_added = True
            except AssignmentError:
                # Means the the assignment for this generation is not possible.
                pass
            except StopIteration:
                # When the end of the possible locations generation is reached.
                raise Exception("Can't add compound {0} to this block space.".format(compound))

    def is_location_out_of_bounds(self, location):
        """
        Check if a location is not outside of the bounds of this block-space.
        """
        for location_d, size_d in zip(location, self.size):
            if location_d < 0:
                return True
            if location_d > size_d - 1:
                return True

    def possible_locations_for(self, compound):
        """
        Generate possible location in which a compound can stand at.
        """
        for x in xrange(self.size[0]):
            for y in xrange(self.size[1]):
                for z in xrange(self.size[2]):
                    yield Location(x, y, z)

        raise AssignmentError("Can't find location for compound {0}.".format(compound))

    def assign_coordinates(self, location, compound):
        """
        For each block in the compound, assign a coordinate for it.
        """

        for i, block in enumerate(compound.blocks):
            assigned_location = None

            # try to assign location.
            for vec in direction.vectors.values():
                possible_location = location + (vec * i)
                if not (possible_location in self.blocks.values() or self.is_location_out_of_bounds(possible_location)):
                    assigned_location = possible_location
                    break

            # If no location was assigned
            if not assigned_location:
                raise AssignmentError("No assignment found for {0}.".format(block))

            yield block, assigned_location

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

        return (min_x, min_y, min_z), (max_x, max_y, max_z)


class AssignmentError(BaseException):
    """
    Thrown when the block space cannot assign coordinates for a compound in a specific location.
    """
    pass
