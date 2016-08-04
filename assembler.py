from pymclevel import nbt
from pymclevel import box
from pymclevel import MCSchematic
from block import CommandBlock

# For development only.
def tagged_cb(command_block, location):
    """
    Translate a command block into a tile entity.
    """
    root_tag = nbt.TAG_Compound()

    root_tag["id"] = nbt.TAG_String("Control")
    # Set the location of the command block.
    root_tag["x"] = nbt.TAG_Int(location[0])
    root_tag["y"] = nbt.TAG_Int(location[1])
    root_tag["z"] = nbt.TAG_Int(location[2])

    # Parse the command of the command block.
    command = command_block.command
    if not isinstance(command, str):
        command = command()
    root_tag["command"] = nbt.TAG_String(command)

    # Return the tag which represents the entity of the command block.
    return root_tag


def translate(location, block):
    """
    Receievs a block object and returns it in NBT tag form
    """
    translated = None

    if isinstance(block, CommandBlock):
        translated = tagged_cb(block, location)

    if translated is None:
        raise Exception("Could not translate block {0} at the location of {1}.".format(block, location))

    return translated


def build(block_space):
    # Create a schematic of the size of the blockspace.
    schematic = MCSchematic(shape=block_space.size)
    entities_to_add = []
    schematic_size = block_space.size
    schematic_box = box.BoundingBox(size=schematic_size)

    for (chunk, _, _) in schematic.getChunkSlices(schematic_box):
        for block, location in block_space.blocks.items():
            # Create the actual block.
            schematic.setBlockAt(location[0], location[1], location[2], block.block_id)
            if block.has_tile_entity:
                # Create the tile entity of the block, if it has one.
                tile_entity = translate(location, block)
                entities_to_add.append((chunk, tile_entity))

    for (chunk, entity) in entities_to_add:
        chunk.TileEntities.append(entity)
        chunk.dirty = True

    return schematic
