"""
Holds all the tuples which hold data about block assignments and compound locations.
"""
from collections import namedtuple

# Holds data for block assignment inside the area and the blockspace internals.
BlockAssignment = namedtuple('BlockAssignment', ['block', 'location', 'direction'])
# Holds data for compound, mainly the location of the compound and what blocks are assigned to it.
AreaAssignment = namedtuple('CompoundAssignment', ['location', 'block_assignments'])
