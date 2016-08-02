from random import randint
from pymclevel import MCSchematic
from pymclevel import TAG_Compound
from pymclevel import nbt

def finalize_cba():
    """
    Gets a CBA, organizes it according to its rules,
    and returns a tuple containing the organized CBA
    and the space it takes.
    (organized_cba, length)

    DEV NOTE: We'll need to add default padding around it.
              like add 1 to the height and width no matter what.
    """
    return (None, 10)


def place_block(block, schematic):
    pass


def populate_block_space(cba_list, block_space):
    cba_list = sorted(cba_list, reverse=True)
    print cba_list

def tagged_cb():
    root_tag = nbt.TAG_Compound()
    root_tag["id"] = nbt.TAG_String("minecraft:chain_command_block")
    root_tag["x"] = nbt.TAG_Int(0)
    root_tag["y"] = nbt.TAG_Int(0)
    root_tag["z"] = nbt.TAG_Int(0)
    root_tag["command"] = nbt.TAG_String("say Hello")
    return root_tag

def main():
    schematic = MCSchematic(shape=(3,3,3))
    schematic.setBlockAt(0, 0, 0, 210)
    schematic.saveToFile(r'C:/new.schematic')

if __name__ == "__main__":
    main()