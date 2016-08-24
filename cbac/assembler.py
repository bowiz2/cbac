from pymclevel import MCSchematic
from pymclevel import TileEntity
from pymclevel import nbt
from block import CommandBlock


def tagged_cb(command_block, location, blockspace):
    """
    Translate a command block into a tile entity.
    :param command_block: The command block you want to translate.
    :param location: the location of the block in the blockspace.
    :param blockspace: the blockspace at which the command block is located.
    :return: nbt tag
    """
    root_tag = nbt.TAG_Compound()

    root_tag["id"] = nbt.TAG_String("Control")

    if command_block.custom_name is not None:
        root_tag["CustomName"] = nbt.TAG_String(command_block.custom_name)
    if command_block.always_active:
        root_tag['auto'] = nbt.TAG_Byte(1)

    root_tag["facing"] = nbt.TAG_String(command_block.facing)
    # Set the location of the command block.
    TileEntity.setpos(root_tag, location)
    # Parse the command of the command block.
    command = command_block.command
    if not isinstance(command, str):
        context = command.command_shell.context
        context.executor = command_block
        context.blockspace = blockspace
        if command.is_conditional:
            command_block.conditional = True
        command = command()

    root_tag["Command"] = nbt.TAG_String(command)
    root_tag["conditional"] = nbt.TAG_Byte(1 if command_block.conditional else 0)

    # Return the tag which represents the entity of the command block.
    return root_tag


def tagged_entity(entity, location, blockspace):
    # TODO: implemnet.
    pass


def translate(block, location, blockspace):
    """
    Takes a block and returns its NBT tag form
    :param block: block you want to translate.
    :param location: the location the block is located in the blockspace.
    :param blockspace: the blockspace the location is at.
    :return: NBT tag.
    """
    translated = None

    if isinstance(block, CommandBlock):
        translated = tagged_cb(block, location, blockspace)

    if translated is None:
        raise Exception("Could not translate block {0} at the location of {1}.".format(block, location))

    return translated


def calculate_data_value(block):
    """
    Generate the data value out of a Block instance.
    :param block: Block
    :return: number
    """
    try:
        return block.data_value
    except AttributeError:
        return 0


def build(block_space):
    """
    Build a blockspace into a schematic
    :param block_space: Blockspace
    :return: MCSchematic containing all the blocks described in the blockspace.
    """
    # Create a schematic of the size of the blockspace.
    schematic = MCSchematic(shape=block_space.size)
    tile_entities_to_add = []

    for block, location in block_space.packed_blocks.items():
        # Create the actual block.
        schematic.setBlockAt(location[0], location[1], location[2], block.block_id)

        data_value = calculate_data_value(block)
        if data_value is not None:
            schematic.setBlockDataAt(location[0], location[1], location[2], data_value)

        if block.has_tile_entity:
            # Create the tile entity of the block, if it has one.
            tile_entity = translate(block, location, blockspace=block_space)
            tile_entities_to_add.append(tile_entity)

    for tile_entity in tile_entities_to_add:
        schematic.addTileEntity(tile_entity)

    return schematic
