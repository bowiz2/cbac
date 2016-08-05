from pymclevel import nbt
from pymclevel import MCSchematic
from pymclevel import TileEntity
from block import CommandBlock
from constants.direction import DOWN, UP, NORTH,SOUTH, WEST, EAST
import struct


# For development only.
def tagged_cb(command_block, location):
    """
    Translate a command block into a tile entity.
    """
    root_tag = nbt.TAG_Compound()

    root_tag["id"] = nbt.TAG_String("Control")
    root_tag["conditional"] = nbt.TAG_Byte(1 if command_block.conditional else 0)

    if command_block.always_active:
        root_tag['auto'] = nbt.TAG_Byte(1)

    root_tag["facing"] = nbt.TAG_String(command_block.facing)
    # Set the location of the command block.
    TileEntity.setpos(root_tag, location)
    # Parse the command of the command block.
    command = command_block.command
    if not isinstance(command, str):
        command = command()
    root_tag["Command"] = nbt.TAG_String(command)

    # Return the tag which represents the entity of the command block.
    return root_tag


def translate(block, location):
    """
    Receievs a block object and returns it in NBT tag form
    """
    translated = None

    if isinstance(block, CommandBlock):
        translated = tagged_cb(block, location)

    if translated is None:
        raise Exception("Could not translate block {0} at the location of {1}.".format(block, location))

    return translated


def calculate_data_value(block):
    if isinstance(block, CommandBlock):
        command_block = block
        faceindex = [DOWN, UP, NORTH, SOUTH, WEST, EAST].index(command_block.facing)
        conditional = 0x8 if command_block.conditional else 0
        data_value = faceindex | conditional
        return data_value


def build(block_space):
    """
    Converts a block space into a schematic.
    """
    # Create a schematic of the size of the blockspace.
    schematic = MCSchematic(shape=block_space.size)
    tile_entities_to_add = []

    for block, location in block_space.blocks.items():
        # Create the actual block.
        schematic.setBlockAt(location[0], location[1], location[2], block.block_id)
        schematic.setBlockDataAt(location[0], location[1], location[2], calculate_data_value(block))
        if block.has_tile_entity:
            # Create the tile entity of the block, if it has one.
            tile_entity = translate(block, location)
            tile_entities_to_add.append(tile_entity)

    for entity in tile_entities_to_add:
        schematic.TileEntities.append(entity)

    return schematic
