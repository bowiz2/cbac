from pymclevel import nbt
from pymclevel import box
from pymclevel import MCSchematic


# For development only.
def tagged_cb():
    root_tag = nbt.TAG_Compound()
    root_tag["id"] = nbt.TAG_String("Control")
    root_tag["x"] = nbt.TAG_Int(0)
    root_tag["y"] = nbt.TAG_Int(0)
    root_tag["z"] = nbt.TAG_Int(0)
    root_tag["command"] = nbt.TAG_String("say Hello")
    return root_tag


def translate(location, block):
    """Receievs a block object and returns it in NBT tag form"""
    return tagged_cb()


# Don't know if this will be needed.
def _get_block_space_size(block_space):
    return (3, 3, 3)


def build(block_space):
    # Create a schematic of the size of the blockspace.
    schematic = MCSchematic(shape=block_space.size)
    ents_to_add = []
    schematic_size = _get_block_space_size(block_space)
    schematic_box = box.BoundingBox(size=schematic_size)
    for (chunk, _, _) in schematic.getChunkSlices(schematic_box):
        for location, block in block_space.items():
            new_ent = translate(location, block)
            schematic.setBlockAt(location[0], location[1], location[2], 137)
            ents_to_add.append((chunk, new_ent))

    for (chunk, entity) in ents_to_add:
        chunk.TileEntities.append(entity)
        chunk.dirty = True
    return schematic
