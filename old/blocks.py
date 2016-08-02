from utils import Location

block_ids = {
	"command_block" : 137,
	"repeating_command_block" : 210,
	"chain_command_block" :211,
}

class Block():
	def __init__(self, minecraft_type):
		self.minecraft_type = minecraft_type
		self.block_id = block_ids.get(minecraft_type, None)
	def __str__(self):
		return self.minecraft_type


class _CommandBlock(object):
	def __init__(self, command, facing, allways_active, conditinal):
		self.command = command
		self.allways_active = allways_active
		self.facing = facing
		self.conditinal = conditinal


class ImpulseCommandBlock(_CommandBlock, Block):
	def __init__(self, command, facing, allways_active=False, conditinal=False):
		_CommandBlock.__init__(self, command, allways_active, facing, conditinal)
		Block.__init__(self, "command_block")


class RepeatCommandBlock(_CommandBlock, Block):
	def __init__(self, command, facing):
		_CommandBlock.__init__(self, command, allways_active=True, conditional=False)
		Block.__init__(self, "repeating_command_block", allways_active=allways_active, facing=facing)


class ChainCommandBlock(_CommandBlock, Block):
	def __init__(self, command, facing):
		_CommandBlock.__init__(self, command, allways_active=True, conditional=False)
		Block.__init__(self, "chain_command_block", allways_active=allways_active, facing=facing, conditional= conditinal)

		

