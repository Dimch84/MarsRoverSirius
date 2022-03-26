class Cell:
	"""
	This class contains information about cell
	Properties:
		x - cell's x-coordinate 
		y - cell's y-coordinate
		is_lock - lock information:
			True - cell is locked
			False - cell is unlocked
	"""

	def __init__(self, x: int, y: int, symbol: chr):
		self.x = x
		self.y = y
		if symbol == '0':
			self.is_lock = False
		else:
			self.is_lock = True

	def get_cell_coord(self):
		return (self.x, self.y)

	def __hash__(self):
		return tuple((self.x, self.y)).__hash__()

	def __eq__(self, other_cell):
		return self.x == other_cell.x and self.y == other_cell.y

