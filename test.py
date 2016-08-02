import block
from constants.direction import *
from constants import cb_action
cb = block.CommandBlock("/say hello", facing=SOUTH, action=cb_action.CHAIN)