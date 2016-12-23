from pymclevel import MCSchematic
from pymclevel import TileEntity
from pymclevel import nbt

from cbac.core.block import CommandBlock
from cbac.core.mc_command import factory as command_factory


def tagged_cb(command_block, location, blockspace):
    """
    Translate a command block into a tile mcentity.
    :param command_block: The command block you want to translate.
    :param location: the location of the block in the blockspace.
    :param blockspace: the blockspace at which the command block is located.
    :return: nbt tag
    """
    # Extarct the command from the command block.
    command = command_block.command

    # If it is an old-school string command. create a MCCommand object out of it.
    if isinstance(command, str):
        command = command_factory(command)

    # Adjust the context of the command.
    if hasattr(command, "context"):
        context = command.context
        context.executor = command_block
        context.blockspace = blockspace

    # Adjust the properties of the command block as the properties of the command itself.
    adjust_cb_to_command(command_block, command)

    # Compile the command.
    command = command.compile()

    # Create the root tag of the command block.
    root_tag = nbt.TAG_Compound()

    # Set the id to that of the command block which is "Control"
    root_tag["id"] = nbt.TAG_String("Control")

    # Set the custom name of the command block tag if needed.
    if command_block.custom_name is not None:
        root_tag["CustomName"] = nbt.TAG_String(command_block.custom_name)

    if command_block.always_active:
        # Set the always active property of the command block tag
        root_tag['auto'] = nbt.TAG_Byte(1)

    # Set the direction of the command block tag.
    root_tag["facing"] = nbt.TAG_String(command_block.facing)

    # Set the location of the command block tag.
    TileEntity.setpos(root_tag, location)

    root_tag["Command"] = nbt.TAG_String(command)

    root_tag["conditional"] = nbt.TAG_Byte(1 if command_block.conditional else 0)

    # Return the tag which represents the mcentity of the command block.
    return root_tag


def adjust_cb_to_command(command_block, command):
    """
    Set the properties of the command block (host) depending on the command inside of it.
    """
    if command.is_conditional:
        command_block.conditional = True

    if command.is_repeated:
        command_block.action = "repeat"


def tagged_entity(entity, location, blockspace):
    """
    :param entity:
    :param location:
    :param blockspace:
    :return:
    """
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
    if hasattr(block, 'data_value'):
        return block.data_value
    return block.block_data


def assemble(block_space):
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
        if block.has_tile_entity:
            # Create the tile mcentity of the block, if it has one.
            tile_entity = translate(block, location, blockspace=block_space)
            tile_entities_to_add.append(tile_entity)

        schematic.setBlockAt(location[0], location[1], location[2], block.block_id)

        data_value = calculate_data_value(block)

        if data_value is not None:
            schematic.setBlockDataAt(location[0], location[1], location[2], data_value)

    for tile_entity in tile_entities_to_add:
        schematic.addTileEntity(tile_entity)

    return schematic


__all__ = ["assemble"]
