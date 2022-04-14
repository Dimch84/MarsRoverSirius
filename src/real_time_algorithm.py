from heapdict import heapdict

from path_planning_algorithm import Path_planning_algorithm
from cell import Cell

class Real_time_algorithm(Path_planning_algorithm):
	ITERATIONS_LIMIT = 100
	def __init__(self,
		         start_coord: (int, int),
		         goal_coord: (int, int),
		         field_input: [str],
		         expansions_limit: int,
		         edges_dict: dict = None):
		super().__init__(start_coord, goal_coord, field_input, edges_dict)
		self.expansions_limit = expansions_limit
		self.closed = list()
		self.g_value[self.start] = 0

	def _lookahead(self, current_cell: Cell):
		"""
		This method do lookahead search phase under limit of operations
		"""
		self.closed.clear()
		self.g_value.clear()
		self.g_value[current_cell] = 0
		self.priority_queue.clear()
		self._set_priority_value(current_cell)
		expansions_counter = 0
		while len(self.priority_queue) > 0 and self.priority_queue.peekitem()[0] != self.goal and expansions_counter < self.expansions_limit:
			expanded_cell, _ = self.priority_queue.popitem()
			self.closed.append(expanded_cell)
			for next_cell in self.field.get_neigbours(expanded_cell):
				edge_cost = self.field.get_edge_cost(expanded_cell, next_cell)
				new_g_value = self._get_g_value(expanded_cell) + edge_cost
				if new_g_value < self._get_g_value(next_cell):
					self.g_value[next_cell] = new_g_value
					self._set_priority_value(next_cell)
			expansions_counter += 1



	def _set_priority_value(self, cell: Cell):
		"""
		This method assign priority value to given cell 
		"""
		self.priority_queue[cell] = self._calculate_priority_value(cell)

	def _calculate_priority_value(self, cell: Cell) -> (int, int):
		"""
		This method calculates priority value of given cell
		"""
		g_value = self._get_g_value(cell)
		return (g_value + self._get_heuristic_value(cell), g_value)

	def _extract_best_cell(self) -> (Cell, int):
		"""
		This method returns cell with best priority and its key
		"""
		return self.priority_queue.peekitem()

	def _update(self, f_value: int):
		"""
		This method updates heuristic values of all expanded cell on current cycle iteration
		"""
		for cell in self.closed:
			self.heuristic_value[cell] = f_value - self._get_g_value(cell)

	def _find_shortest_path(self, current_cell: Cell, next_cell: Cell) -> [Cell]:
		"""
		This method recovers optimal path from current cell to next cell
		"""
		cell_on_the_path = next_cell
		path = [cell_on_the_path]
		while cell_on_the_path != current_cell:
			previous_cell = None
			min_g_value = self.INFINITY
			for cell in self.field.get_neigbours(cell_on_the_path):
				if self._get_g_value(cell) < min_g_value:
					min_g_value = self._get_g_value(cell)
					previous_cell = cell 
			path.append(previous_cell)
			cell_on_the_path = previous_cell
		return path[::-1]


	def run(self) -> [Cell]:
		"""
		This method performs general lookahead-update-act cycle of any real-time algorithm
		"""
		current_cell = self.start
		path_to_goal_cell = [current_cell]
		iterations_counter = 0
		while current_cell != self.goal and iterations_counter < self.ITERATIONS_LIMIT:
			iterations_counter += 1
			self._lookahead(current_cell)
			if len(self.priority_queue) == 0:
				return None
			next_cell, next_cell_key = self._extract_best_cell()
			self._update(next_cell_key[0])
			path = self._find_shortest_path(current_cell, next_cell)
			for cell in path[1:]:
				path_to_goal_cell.append(cell)
				current_cell = cell
				if cell.is_lock == True:
					break
		if iterations_counter == self.ITERATIONS_LIMIT:
			return None
		return path_to_goal_cell

	@classmethod
	def call(cls,
		     start: (int, int),
		     goal: (int, int),
		     field: [str],
		     expansions_limit: int,
		     edges_dict: dict = None) -> (int, [Cell]):
		"""
		This method call algorithm with given start cell, goal cell, field, edges set and limit of expansions count
		params:
			start - start cell's coordinates
			goal - goal cell's coordinates
			field - matrix view of field where
				'1' - cell is locked
				'0' - cell is unlocked
			expansions_limit - number that limited expansions count on one lookahead phase
			edges_dict - dictionary of all graph edges with their costs
		"""
		algorithm_instance = cls(start, goal, field, expansions_limit, edges_dict) 
		answer_path = algorithm_instance.run()
		if answer_path != None:
			return [cell.get_cell_coord() for cell in answer_path]
		return None

