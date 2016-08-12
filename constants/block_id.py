EMPTY_BLOCK = 0
AIR_BLOCK = EMPTY_BLOCK
GLASS_BLOCK = 20
SNOW_BLOCK = 80
REDSTONE_BLOCK = 152

# A block which represents the "true" value.
TRUE_BLOCK = REDSTONE_BLOCK
# A block which represents the "false" value.
FALSE_BLOCK = SNOW_BLOCK

IMPULSE_COMMAND_BLOCK = 137
REPEATING_COMMAND_BLOCK = 210
CHAIN_COMMAND_BLOCK = 211

# Blocks which do not further redstone signal.
ISOLATORS = [EMPTY_BLOCK, GLASS_BLOCK]

names = {
    GLASS_BLOCK: 'glass',
    EMPTY_BLOCK: 'air',
    SNOW_BLOCK: 'snow',
    REDSTONE_BLOCK: 'redstone_block'
}
