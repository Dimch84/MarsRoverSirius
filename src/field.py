from cell import Cell

STEPS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

class Field:
	"""
	This class contains information about field
	Properties:
		height - field's height
		width - field's width
		desk_info - array reprentatation of desk
		edges_info - dictionary with edges costs
		board - board of cells which represent field state 
	"""
	def __init__(self, height: int, width: int, desk_input: str, edges_dict: dict):
		self.height = height
		self.width = width
		self.desk_info = desk_input
		self.edges_info = edges_dict
		self.board = dict()

	def get_edge_cost(self, cell_1: Cell, cell_2: Cell) -> int:
		if self.edges_info == None:
			return 1
		coord_1, coord_2 = cell_1.get_cell_coord(), cell_2.get_cell_coord()
		return self.edges_info[(min(coord_1, coord_2), max(coord_1, coord_2))]

	def get_cell(self, cell_coord: (int, int)) -> Cell:
		"""
		This method returns cell by given coordinates
		"""
		return self.board.setdefault(cell_coord, Cell(cell_coord[0], cell_coord[1], self.desk_info[cell_coord[0]][cell_coord[1]]))
		
	def get_neigbours(self, cell: Cell) -> [Cell]:
		"""
		This method returns all unlock neigbours of given cell
		"""
		potential_neighbours = [(delta_x + cell.x, delta_y + cell.y) for delta_x, delta_y in STEPS]
		return map(self.get_cell, filter(self._cell_is_good, potential_neighbours))
		
	def calculate_heuristic_value(self, cell, goal_cell) -> int:
		"""
		This method calculates heuristic function for given cell 
		"""
		return max(abs(cell.x - goal_cell.x), abs(cell.y - goal_cell.y))
 

	def _cell_is_good(self, cell_coord: (int, int)) -> bool:
		"""
		This method checks if given cell's coordinates correspond with relevant unlock cell
		"""
		return 0 <= cell_coord[0] < self.height and 0 <= cell_coord[1] < self.width and self.get_cell(cell_coord).is_lock == False

	