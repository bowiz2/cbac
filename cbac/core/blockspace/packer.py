"""
Packs items by their areas.
Note that this module does not account for the destination size.
"""
from cbac.core.blockspace.area_factory import area_factory
from cbac.core.blockspace.assignment import BlockAssignment, AreaAssignment

from cbac.core.utils import Vector


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
    Takes a collection of areas and organizes them together relative to a centralized point.
    :param areas: areas you want to pack.
    :return: dict of area and the location inside the blockspace.
    """
    assignments = {}
    pivot = Vector(0, 0, 0)
    # TODO: adjust to build direction
    for area in areas:
        assignments[area] = pivot
        if area.is_isolated:
            pivot += Vector(0, 0, 1)
        else:
            prev_area_index = areas.index(area) - 1
            if prev_area_index >= 0:
                if areas[prev_area_index].is_isolated:
                    pivot += Vector(0, 0, 1)

        pivot += Vector(0, 0, area.dimensions.z + 1)

    return assignments
