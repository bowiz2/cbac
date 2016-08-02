#search for command blocks, eval what is between the ^^
try:
	from pymclevel 			import TAG_List
	from pymclevel 			import TAG_Byte
	from pymclevel 			import TAG_Int
	from pymclevel 			import TAG_Compound
	from pymclevel 			import TAG_Short
	from pymclevel 			import TAG_Double
	from pymclevel 			import TAG_String
except:
	pass
#import helpers
import const
from blocks import ChainCommandBlock, ImpulseCommandBlock
from utils import Location

DEBUG = False

def log(f):
	global DEBUG
	def _wrapper(*args, **kwargs):
		if DEBUG:
			print "calling", f.__name__, "with", args, kwargs
		ret = f(*args, **kwargs)
		if DEBUG:
			print "returned", ret
		return ret
	return _wrapper



class UnsetLocation(Location):
	def __new__(self):
		pass

displayName = "cdompile"
perm_table_start = (0,53,0)


def area(area):
	return "{} {}".format(*map(point, area))


class RealObject(object):
	"""
	Represents a "real" object in the minecraft world.
	"""
	def __init__(self, location=None, isolated=False):
		if location == None:
			location = UnsetLocation()
		self.location = location
		# if the real object must be built isolated from other redstone.
		self.isolated = isolated
		# All the locations in this object are related to the location of this object.
		self.blocks = dict()

	@log
	def is_collides(self, other):
		"""
		Check if this object collides with other object.
		"""
		for block_location in self.blocks.keys():
			real_location = block_location + self.location
			for other_block_location in other.blocks.keys():
				other_real_location = other_block_location + other.location
				if real_location == other_real_location:
					return True
		return False
	def is_isloated_from(self, other):
		"""
		Check if this real object is isolated from other object
		"""
		return True

	@property
	def is_bound(self):
	    return self.location != None
	

class Constant(RealObject):
	def __init__(self, number, location=None):
		super(Constant, self).__init__(location)
		# lest significant bit is at index 0 .
		self.number= number
		self.bits = [bool(int(x)) for x in reversed(bin(number)[2:])]

		pivot = Location(0,0,0)
		for i, bit in enumerate(self.bits):
			bit_block = const.TRUE_BLOCK if bit else const.FALSE_BLOCK
			self.blocks[pivot + Location(i, 0, 0)] = bit_block

	def __str__(self):
		def bit_to_string(bit):
			if bit:
				return '1'
			else:
				return '0'
		return "Constant<{0}>".format(hex(self.number))


class BlockSpace(object):
	"""
	represent a collection of real objects
	"""
	def __init__(self, location):
		# TODO: do we need borders?
		self.location = location
		self.real_objects = list()

	def bind(self, real_object):
		"""
		Bind the real object to a locaiton.
		"""
		# TODO: fix the location setting.
		assert not isinstance(real_object, UnsetLocation)

		for _y in xrange(120):
			for _x in xrange(50):
				for _z in xrange(50):
				
					# set the location.
					real_object.location= Location(_x, _y, _z)
					
					location_matches = True
					
					# check if the location really matches.
					for other_real_object in self.real_objects:
						if real_object.is_collides(other_real_object):
							location_matches = False
							break
						if real_object.isolated:
							if not real_object.is_isloated_from(other_real_object):
								location_matches = False
								break
					# sucsess.
					if location_matches:
						self.real_objects.append(real_object)
						return real_object
		real_object = None
		raise Exception("bind un-sucssesfull.")

	# unbind function is not needed.
	def build(self):
		for real_object in self.real_objects:
			if not real_object.is_bound:
				self.bind(real_object)

		blocks = {}
		for real_object in self.real_objects:
			for location, block in real_object.blocks.items():
				real_location = location + real_object.location + self.location
				if real_location in blocks.keys():
					raise Exception("Build exception")
				blocks[real_location] = block
		return blocks


class CBA(RealObject):
	def __init__(self, command_blocks, location=None):
		# the command chain must be isolated, becuase it contains command blocks.
		super(CBA, self).__init__(location, isolated=True)
		# cb stends for command block.
		self.first_cb_location = Location(0,0,0)

		for i, cb in enumerate(command_blocks):
			pivoted_location = self.first_cb_location + (i, 0, 0)
			cb.facing = "east"
			self.blocks[pivoted_location] = cb
		
		self.last_cb_location = pivoted_location

		self.exit_direction = (1, 0, 0)


def command_chain(*commands):
	assert len(commands) > 0

	yield ImpulseCommandBlock(commands[0], None)
	
	for command in commands[1:]:
		yield ChainCommandBlock(command, allways_active=True)

bs = BlockSpace(Location(0, 56, 0))
c = Constant(4)
y = Constant(7)
y = bs.bind(y)
c = bs.bind(c)
cba = CBA(command_chain("/say what"))
bs.bind(cba)
print bs.build()

def perform(level, box, options):
	entsToAdd = []
	cbs_to_create = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities if tileents else chunk.Entities:
			for location, cb in bs.blocks.items():
					newcommand = TAG_Compound()
					newcommand["id"] = TAG_String("Control")
					newcommand["x"] = TAG_Int(location.x)
					newcommand["y"] = TAG_Int(location.y)
					newcommand["z"] = TAG_Int(location.z)
					newcommand["Command"] = cb.command
					newcommand["conditional"] = cb.conditional
					newcommand["facing"] = cb.facing

					#newcommand["CustomName"] = e["CustomName"]
					level.setBlockAt(x, y, z, cb.block_id)
					level.setBlockDataAt(x, y, z, 1 if cb.allways_active else 0)
					entsToAdd.append((chunk,newcommand))
					entsToDelete.append((chunk, e))

	for (chunk, entity) in entsToAdd:
		if not tileents:
			chunk.TileEntities.append(entity)
		else:
			chunk.Entities.append(entity)
		chunk.dirty = True
				
	for (chunk, entity) in entsToDelete:
		if tileents:
			chunk.TileEntities.remove(entity)
		else:
			chunk.Entities.remove(entity)
		chunk.dirty = True

