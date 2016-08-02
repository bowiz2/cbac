# CABC
## Project Goal
###Write a python wrapper for creating command block arrays in minecraft.

**Basic Blocks** - Command Blocks and Data Blocks
  * Contains block id and data

**Block Compounds** - Command Block Arrays and Memory Slots
  * Contains the blocks which are part of the compound.

**Block Space** - Logical representation of blocks in the world
  * Receives a group of Block Compounds.
  * Goes over all Compounds and assigns them coordinates in the blockspace.

**Translator** - Takes logical representations and converts them to Minecraft Blocks and TileEntities
  * Goes over every Command Block in the blockspace and calls the command function.
  * Takes a block space and converts every pythonic object into a TileEntity and Minecraft Block.

**Builder** - Takes Minecraft Blocks and TileEntities and places them into the world.
  * Takes Minecraft Blocks and TileEntities and places them into the world based on their supplied positions.
