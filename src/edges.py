from src.cell import Cell
from src.field import Field

class Edges:
	"""
	This class contains information about edges in the graph
	Properties:
		list_of_neigbours[cell]: contains all neigbours of given cell with edges costs
	"""

	def __init__(self):
		self.list_of_neigbours = dict()

	def _add_edge(self, cell_1: Cell, cell_2: Cell, weight: int):
		"""
		This private method add edge with given weight between cell_1 and cell_2
		"""
		self.list_of_neigbours.setdefault(cell_1, {})[cell_2] = weight
		self.list_of_neigbours.setdefault(cell_2, {})[cell_1] = weight

	def appoint_unit_edges_costs(self, field: Field):
		"""
		This method appoints every edge in the field unit cost
		"""
		for cell in field.get_board():
			if cell.is_lock == True:
				continue
			for neigbour_cell in field.get_neigbours(cell):
				self._add_edge(cell, neigbour_cell, 1)

	def get_neigbours(self, cell: Cell) -> dict:
		"""
		This method returns all neigbours with edges costs to them of given cell
		"""
		return self.list_of_neigbours.setdefault(cell, {}).items()

	def get_edge_cost(self, cell_1: Cell, cell_2: Cell) -> int:
		return self.list_of_neigbours[cell_1][cell_2]

	@staticmethod
	def set_edges(edges_dict: dict, field: Field):
		"""
		This method transform dictionary with edges into Edges instance
		"""
		edges = Edges()
		if edges_dict == None:
			edges.appoint_unit_edges_costs(field)
		else:
			for (cell_coord_1, cell_coord_2), weight in edges_dict.items():
				edges._add_edge(field.get_cell(cell_coord_1), field.get_cell(cell_coord_2), weight)
		return edges
		