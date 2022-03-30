from heapdict import heapdict

from cell import Cell
from field import Field
from edges import Edges

class Path_planning_algorithm:
	INFINITY = 1000

	@classmethod
	def call(cls,
		     start: (int, int),
		     goal: (int, int),
		     field: [str],
		     edges_dict: dict = None):
		algorithm_instance = cls(start, goal, field, edges_dict) 
		answer = algorithm_instance._compute_shortest_path()
		if answer == Path_planning_algorithm.INFINITY:
			return None, None
		path = algorithm_instance._find_shortest_path()
		return answer, [cell.get_cell_coord() for cell in path]

	def __init__(self,
		         start_coord: (int, int),
		         goal_coord: (int, int),
		         field_input: [str],
		         edges_dict: dict = None):
		height, width = len(field_input), len(field_input[0])
		self.field = Field(height, width, field_input)
		self.start = self.field.get_cell(start_coord)
		self.goal = self.field.get_cell(goal_coord)
		self.edges = Edges.set_edges(edges_dict, self.field)
		self.heuristic_value = dict()
		self.g_value = dict()
		self.priority_queue = heapdict()

	def _init(self):
		self._set_priority_value(self.start)

	def _get_heuristic_value(self, cell: Cell):
		return self.heuristic_value.setdefault(cell, self.field.calculate_heuristic_value(cell, self.goal))

	def _get_g_value(self, cell: Cell):
		return self.g_value.setdefault(cell, self.INFINITY)

	def _set_priority_value(self, cell: Cell):
		self.priority_queue[cell] = self._calculate_priority_value(cell)


	def _find_shortest_path(self) -> [Cell]:
		cell_on_the_path = self.goal
		path = [cell_on_the_path]
		while cell_on_the_path != self.start:
			previous_cell = None
			min_g_value = self.INFINITY
			for cell in self.field.get_neigbours(cell_on_the_path):
				if self._get_g_value(cell) < min_g_value:
					min_g_value = self._get_g_value(cell)
					previous_cell = cell 
			path.append(previous_cell)
			cell_on_the_path = previous_cell
		return path[::-1]

