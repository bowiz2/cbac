from random import randint
from pymclevel import MCSchematic
from pymclevel import nbt
from pymclevel import box

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


def build(schematic, block_space):
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

def main():
    schematic = MCSchematic(shape=(3,3,3))
    block_space = {(0, 0, 0): "not_a_block"}            
    schematic = build(schematic, block_space)
    schematic.saveToFile(r'./MCEdit/MCEdit 2 Files/schematics/3new.schematic')

if __name__ == "__main__":
    main()