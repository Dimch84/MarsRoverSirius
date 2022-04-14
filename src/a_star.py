from heapdict import heapdict

from cell import Cell
from path_planning_algorithm import Path_planning_algorithm

class A_star(Path_planning_algorithm):
	"""
	This is child class of parental class Path_planning_algorithm dedicated to A* algorithm, 
	it inherits some parental class behaviour, but also have its own features  
	"""
	def __init__(self,
		         start_coord: (int, int),
		         goal_coord: (int, int),
		         field_input: [str],
		         edges_dict: dict = None):
		super().__init__(start_coord, goal_coord, field_input, edges_dict)
		self.g_value[self.start] = 0
		self._set_priority_value(self.start)
		
	def _calculate_priority_value(self, cell: Cell) -> (int, int):
		g_value = self._get_g_value(cell)
		return (g_value + self._get_heuristic_value(cell), g_value)
	
	def _compute_shortest_path(self) -> int:
		"""
		This method computes length of the shortest path from start cell to goal cell
		"""
		while len(self.priority_queue) > 0 and self.priority_queue.peekitem()[0] != self.goal:
			current_cell, _ = self.priority_queue.popitem()
		
			for next_cell in self.field.get_neigbours(current_cell):
				edge_cost = self.field.get_edge_cost(current_cell, next_cell)
				new_g_value = self._get_g_value(current_cell) + edge_cost
				if new_g_value < self._get_g_value(next_cell):
					self.g_value[next_cell] = new_g_value
					self._set_priority_value(next_cell)

		return self._get_g_value(self.goal) 

	




