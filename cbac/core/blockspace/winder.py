"""
Winds an array of command blocks into a compact area.
"""
import math
from cbac.core.block import CommandBlock, Block, BlockID
from cbac.core.blockspace.assignment import BlockAssignment
from cbac.core.mc_direction import MCDirection

from cbac.core.utils import Vector

PAD_BLOCK = BlockID.EMERALD_BLOCK


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

    row_locations = list(locate_rows(rows))
    directions = decide_directions(rows, build_direction, row_locations)

    locs = locate_blocks(rows, row_locations)

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
            construction_row.append(CommandBlock("", action="chain"))

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
        row.append(Block(PAD_BLOCK))


def decide_directions(rows, start_direction, row_locations):
    """
    For each row, decide the directions its blocks are facing. Also reverse rows if needed.
    :param rows: rows you want to change the directions for.
    :param start_direction: the direction of the first row.
    :return: decided directions for each block.
    """
    directions = {}
    # set directions for the blocks.
    for row_id, row in enumerate(rows):

        for block in row:
            if block is not row[-1]:
                directions[block] = [start_direction, MCDirection.opposite(start_direction)][row_id % 2]
            else:
                if row_id + 1 < len(rows):
                    direction = MCDirection.from_vector(row_locations[row_id + 1] - row_locations[row_id])
                    if direction not in [MCDirection.UP, MCDirection.DOWN]:
                        direction = MCDirection.opposite(direction)
                    directions[block] = direction
                else:
                    directions[block] = MCDirection.UP
        if row_id % 2 is 1:
            row.reverse()
    return directions


def locate_rows(rows):
    height = int(math.sqrt(len(rows)))
    while len(rows) % height < (height / 2):
        height -= 1
    pivot = Vector(0, 0, 0)
    direction = 1

    for i, row in enumerate(rows):
        yield pivot

        if pivot.y % height == 0 and i is not 0:
            direction *= -1
            pivot += (0, 0, 1)
            yield pivot

        pivot += Vector(0, direction, 0)


def locate_blocks(rows, row_locations):
    """
    Calculate the locations of each block in the rows.
    :param rows: collection of rows.
    :return: dict of locations.
    """
    locations = {}
    # set locations for the blocks.
    for row, row_location in zip(rows, row_locations):
        for block_id, block in enumerate(row):
            locations[block] = row_location + Vector(block_id, 0, 0)
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
