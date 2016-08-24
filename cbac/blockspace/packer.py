from .assignment import BlockAssignment, AreaAssignment
from .area_factory import area_factory
from cbac.utils import Vector


def pack(items):
    """
    Takes a collection of items and packs them into a small space.
    :return: dict of area assignments.
    """
    areas = [area_factory(item) for item in items]

    area_assignments = {}
    packed_areas = pack_areas(areas)
    for area, area_location in packed_areas.items():
        my_assignment = AreaAssignment(
            location=area_location,
            block_assignments=[BlockAssignment(block, area_location + relative_block_location, block_direction)
                               for block, relative_block_location, block_direction in area.packed_blocks]
        )

        area_assignments[area.wrapped] = my_assignment

    return area_assignments


def pack_areas(areas):
    """
    Takes a collection of areas and organizes them inside the
    :param areas:
    :return: dictionary of area and the location inside the blockspace.
    """
    # Sort the areas by height, greatest height first
    sorted_areas = sorted(areas, key=lambda area: area.dimensions[2], reverse=True)
    # Make a packing space the height of the tallest area.
    packing_height = sorted_areas[0].z
    assignments = {}
    x_offset = 0

    while len(sorted_areas) > 0:
        root_area = sorted_areas.pop()
        column = _build_column(root_area, sorted_areas, packing_height)
        column_dict = _column_to_dict(column, x_offset)
        for key in column_dict:
            assignments[key] = column_dict[key]
        x_offset += root_area.dimensions[0]
    return assignments


def _build_column(root_area, sorted_areas, packing_height):
    """ Returns a list of areas for the column, from top to bottom."""
    res = [root_area]
    height_left = packing_height - root_area.dimensions[2]
    while height_left > 0:
        index = _find_suitable_child(sorted_areas, height_left, root_area.dimensions[2])
        if index == -1:
            return res
        child = sorted_areas.pop(index)
        res.append(child)
        height_left -= child.z
    return res


def _column_to_dict(column, x_offset):
    res = {}
    z_offset = 0
    for i in xrange(len(column)):
        area = column[i]
        res[area] = (x_offset, area.dimensions[2] + z_offset)
        z_offset += area.dimensions[2]
    return res


def _find_suitable_child(sorted_areas, max_z, max_x):
    """
    Goes over sorted_areas, finding a suitable area to place the next area in the column.
    Can be a binary search when I feel like implementing it.
    :return: If found, the index of the area. Else, -1.
    """
    for i in xrange(len(sorted_areas) - 1):
        if sorted_areas[i + 1].z - max_z < 0 and sorted_areas[i + 1].x < max_x:
            return i
    return -1


