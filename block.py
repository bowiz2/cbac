from constants.block_id import CHAIN_COMMAND_BLOCK, IMPULSE_COMMAND_BLOCK, REPEATING_COMMAND_BLOCK

class Block(object):
    def __init__(self, block_id, block_data):
        self.block_id = block_id
        self.block_data = block_data


class CommandBlock(Block):
    def __init__(self, command, facing, action="impulse", always_active=False, conditional=False):

        self.facing = facing
        self.action = action
        self.always_active = always_active
        self.conditional = conditional

        if self.action == "impulse":
            block_id = 137
        elif self.action == "repeat":
            block_id = 210
        elif self.action == "chain":
            block_id = 211
        else:
            raise TypeError("No such action {0}.".format(action))

        block_data = 1 if self.always_active else 0

        super(CommandBlock, self).__init__(block_id, block_data)
