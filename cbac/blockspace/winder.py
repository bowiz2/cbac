"""
Winds an array of command blocks into a compact area.
"""
from cbac.block import CommandBlock
from cbac.constants import mc_direction
from cbac.blockspace.assignment import BlockAssignment
from cbac.utils import Vector


# TODO: provide better doc.
# TODO: breakdown to samller  functions
def winde(compound, max_width, start_build_direction):
    build_direction = start_build_direction
    # Matrix of rows.
    rows = []
    row = []
    # All the blocks of the compound.
    total_blocks = list(compound.blocks)
    # Generate rows from blocks.
    for i, block in enumerate(total_blocks):
        if len(row) is max_width - 1:
            row.append(CommandBlock("/say padding", action="chain"))

        if len(row) is max_width:
            rows.append(row)
            row = [CommandBlock(rows[-1][-2].shell.has_succeeded(), action="chain", always_active=True)]
        row.append(block)

    rows.append(row)

    # pad last row with nones
    last_row = rows[-1]
    for i in xrange(max_width - len(last_row)):
        # Append none for operation
        last_row.append(None)

    directions = {}
    locs = {}
    # set directions for the blocks.
    for row_id, row in enumerate(rows):
        for block in row:
            if block is not row[-1]:
                directions[block] = [build_direction, mc_direction.oposite(build_direction)][row_id % 2]
            else:
                directions[block] = mc_direction.UP

        if row_id % 2 is 1:
            row.reverse()

    # set locations for the blocks.
    for row_id, row in enumerate(rows):
        for block_id, block in enumerate(row):
            locs[block] = Vector(block_id, row_id, 0)

    derowed_blocks = []

    for row in rows:
        for block in row:
            if block is not None:
                derowed_blocks.append(block)

    # compile assignments
    return [BlockAssignment(block, locs[block], directions[block]) for block in derowed_blocks]