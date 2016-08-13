from compound import CBA
from constants import direction
from constants.block_id import ISOLATORS
from utils import Location


class PackingError(BaseException):
    """
    Thrown when the block space cannot assign coordinates for a compound in a specific location.
    """
    pass


def location_gen(compound, blockspace):
    for x in xrange(blockspace.size[0]):
        for y in xrange(blockspace.size[1]):
            for z in xrange(blockspace.size[2]):
                yield Location(x, y, z)


def pack(compound, blockspace, spec_location, start_build_direction):
    """
    Try to pack a compound at a location in a blockspace
    """
    def try_pack(location):
        current_build_direction = start_build_direction
        # For each block try to assign location and hope for the location to match.
        for i, block in enumerate(compound.blocks):
            # check if this block allready have been assigned location.
            if block in blockspace.blocks:
                yield (block, (blockspace.blocks[block], blockspace.directions[block]))
            else:
                # assign new location.
                # try to assign location.
                direction_vector = direction.vectors[current_build_direction]

                possible_location = location + (direction_vector * i)

                if possible_location in blockspace.blocks.values():
                    raise PackingError("Collision with block at location {0}".format(possible_location))

                if blockspace.is_location_out_of_bounds(possible_location):
                    raise PackingError("Location out of bounds.")

                if compound.isolated and not blockspace.is_isolated(possible_location):
                    raise PackingError("Location not isolated while isolation is required.")

                if block.block_id not in ISOLATORS:
                    for isolated_location in blockspace._isolated_blocks_locations:
                        if isolated_location.is_adjacent(possible_location):
                            raise PackingError("Location interferes with the isolation of other compounds.")

                assigned_location = possible_location

                yield (block, (assigned_location, current_build_direction))

    if spec_location is None:
        for location in location_gen(compound, blockspace):
            try:
                return dict(try_pack(location))
            except PackingError:
                pass
        raise PackingError
    return dict(try_pack(spec_location))