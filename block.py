class Block(object):
    def __init__(self, block_id, block_data):
        self.block_id = block_id
        self.block_data = block_data


class CommandBlock(Block):
    def __init__(self, command, facing, action="impuls", allways_active=False, conditional=False):

        self.facing = facing
        self.action = action
        self.allways_active = allways_active
        self.conditional = conditional

        if self.action == "impulse":
            block_id = 137
        elif self.action == "repeat":
            block_id = 210
        elif self.action == "chain":
            block_id = 211
        else:
            raise TypeError("No such action {0}.".format(action))

        block_data = 1 if self.allways_active else 0

        super(CommandBlock, self).__init__(block_id, block_data)