"""
Winds an array of command blocks into a compact area.
"""
from cbac.block import CommandBlock
from cbac.constants import mc_direction
from cbac.blockspace.assignment import BlockAssignment
from cbac.utils import Vector


def winde(blocks, max_width, start_build_direction):
    """
    Winds an array of command blocks into a compact area.
    :param blocks: list of blocks you want to wind.
    :param max_width: the maximum with to which to winde.
    :param start_build_direction: to which the blocks are ought to be winded.
    :return: list of block assignments.
    """
    build_direction = start_build_direction

    rows = generate_rows(blocks, max_width)

    # Pad last row.
    _pad(rows[-1], max_width)

    directions = decide_directions(rows, build_direction)

    locs = locate_blocks(rows)

    return [BlockAssignment(block, locs[block], directions[block]) for block in extract_blocks(rows)]


def generate_rows(blocks, row_length):
    """
    Generate a matrix of rows. pad them with condition-passing command blocks if needed.
    :param blocks: blocks you want to places in the rows.
    :param row_length: max row length of the generated rows. It is not promised that these rows have the same size.
    :return: rows list.
    """
    # Matrix of rows.
    rows = []
    construction_row = []

    for i, block in enumerate(blocks):

        if len(construction_row) is row_length - 1:
            construction_row.append(CommandBlock("/say padding", action="chain"))

        if len(construction_row) is row_length:
            rows.append(construction_row)
            construction_row = [CommandBlock(rows[-1][-2].shell.has_succeeded(), action="chain", always_active=True)]

        construction_row.append(block)

    rows.append(construction_row)

    return rows


def _pad(row, complete_size):
    """
    Fill the row with nodes so the length of the row will reach the complete_size.
    :param row: The row you want to pad.
    :param complete_size: The size of the row at which there is no need to pad it.
    :return: row after padding.
    """
    while len(row) < complete_size:
        row.append(None)


def decide_directions(rows, start_direction):
    """
    For each row, decide the directions its blocks are facing. Also reverse rows if needed.
    :param rows: rows you want to change the directions for.
    :param start_direction: the direction of the first row.
    :return: decided directions for each block.
    """
    directions = {}
    # set directions for the blocks.
    for row_id, row in enumerate(rows):

        if row_id % 2 is 1:
            row.reverse()

        for block in row:
            if block is not row[-1]:
                directions[block] = [start_direction, mc_direction.oposite(start_direction)][row_id % 2]
            else:
                directions[block] = mc_direction.UP
    return directions


def locate_blocks(rows):
    """
    Calculate the locations of each block in the rows.
    :param rows: collection of rows.
    :return: dict of locations.
    """
    locations = {}
    # set locations for the blocks.
    for row_id, row in enumerate(rows):
        for block_id, block in enumerate(row):
            locations[block] = Vector(block_id, row_id, 0)
    return locations


def extract_blocks(rows):
    """
    Extract each block from the rows, if it is not None.
    :param rows: collection of rows.
    :return: Generator.
    """
    for row in rows:
        for block in row:
            if block is not None:
                yield block
