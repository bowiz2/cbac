"""
Holds all the block ids which are used in this program and are provided for the user for easier semantics.
"""
EMPTY_BLOCK = 0
AIR_BLOCK = EMPTY_BLOCK
GLASS_BLOCK = 20
SNOW_BLOCK = 80
REDSTONE_BLOCK = 152
EMERALD_BLOCK = 133
# A block which represents the "true" value.
TRUE_BLOCK = REDSTONE_BLOCK
# A block which represents the "false" value.
FALSE_BLOCK = SNOW_BLOCK

# Command block materials.
IMPULSE_COMMAND_BLOCK = 137
REPEATING_COMMAND_BLOCK = 210
CHAIN_COMMAND_BLOCK = 211

# Blocks which do not further redstone signal.
ISOLATORS = [EMPTY_BLOCK, GLASS_BLOCK]

names = {
    GLASS_BLOCK: 'glass',
    EMPTY_BLOCK: 'air',
    SNOW_BLOCK: 'snow',
    REDSTONE_BLOCK: 'redstone_block',
    IMPULSE_COMMAND_BLOCK: 'command_block',
    REPEATING_COMMAND_BLOCK: 'repeating_command_block',
    CHAIN_COMMAND_BLOCK: 'chain_command_block',
    EMERALD_BLOCK: 'emerald_block'
}
