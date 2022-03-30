from path_planning_algorithm import Path_planning_algorithm

from cell import Cell
from field import Field
from edges import Edges

class Lifelong_a_star(Path_planning_algorithm):
	def __init__(self,
		         start_coord: (int, int),
		         goal_coord: (int, int),
		         field_input: [str],
		         edges_dict: dict = None):
		self.rhs_value = dict()
		super().__init__(start_coord, goal_coord, field_input, edges_dict)
		self.rhs_value[self.start] = 0
		super()._init()

	def _calculate_priority_value(self, cell: Cell):
		min_value = min(self._get_rhs_value(cell), self._get_g_value(cell))
		return (min_value + self._get_heuristic_value(cell), min_value)

	def _get_rhs_value(self, cell: Cell):
		return self.rhs_value.setdefault(cell, self.INFINITY)

	def _update_cell(self, cell: Cell):
		if cell != self.start:
			self.rhs_value[cell] = min([self._get_g_value(neigbour) + self.edges.get_edge_cost(neigbour, cell) for neigbour in self.field.get_neigbours(cell)])
		if cell in self.priority_queue.keys():
			self.priority_queue.pop(cell)
		if self._get_rhs_value(cell) != self._get_g_value(cell):
			self._set_priority_value(cell)

	def _compute_shortest_path(self):
		while len(self.priority_queue) > 0:
		 	if self.priority_queue.peekitem()[1] >= self._calculate_priority_value(self.goal):
		 		if self._get_rhs_value(self.goal) == self._get_g_value(self.goal):
		 			break
		 	current_cell, _ = self.priority_queue.popitem()
		 	if self._get_g_value(current_cell) > self._get_rhs_value(current_cell):
		 		self.g_value[current_cell] = self._get_rhs_value(current_cell)
		 		for next_cell in self.field.get_neigbours(current_cell):
		 			self._update_cell(next_cell)
		 	else:
		 		self.g_value[current_cell] = INFINITY
		 		for next_cell in field.get_neigbours(current_cell) + [current_cell]:
		 			self._update_cell(next_cell)
		return self._get_g_value(self.goal)  

