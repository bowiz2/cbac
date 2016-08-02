from collections import namedtuple


class Location(namedtuple('Location', ['x', 'y', 'z'])):
	def __add__(self, other):
		return Location(*[i+j for i,j in zip(self, other)])
	def __str__(self):
		return " ".join(map(str,self))


