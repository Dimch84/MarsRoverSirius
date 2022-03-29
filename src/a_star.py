from heapdict import heapdict
from cell import Cell
from field import Field
from edges import Edges

INFINITY = 1000

class A_star:
	@staticmethod
	def call(start: (int, int),
		     goal: (int, int),
		     field: [str],
		     edges_dict: dict = None) -> (int, [(int, int)]):
		"""
		This method calculates path (and his length) from start cell to goal cell with A* algorithm
		param start: start cell coordinates
		param goal: goal cell cordinates
		param field: matrix of cells with information about lock cells:
			'0' - cell is unlocked
			'1' - cell is locked
		param edges_dict: edges dictionary with their cost 
		"""
		height, width = len(field), len(field[0])
		height, width = len(field), len(field[0])
		field_instance = Field(height, width, field)
		start_cell = field_instance.get_cell(start)
		goal_cell = field_instance.get_cell(goal)
		edges = Edges.set_edges(edges_dict, field_instance)
		answer, path = A_star.get_optimal_path(start_cell, goal_cell, field_instance, edges)
		if answer == None:
			return None, None
		return answer, [cell.get_cell_coord() for cell in path]

	
	@staticmethod
	def get_optimal_path(start: Cell, 
		                 goal: Cell, 
		                 field: Field,
		                 edges: Edges = None) -> (int, [Cell]):
		"""
		This method calculates path (and his length) from start cell to goal cell with A* algorithm
		param start: start cell
		param goal: goal cell
		param field: given Field instance
		param edges: given Edges instance
		"""

		if edges == None: # if Edges instance wasn't passed to method then every edge has unit cost
			edges = Edges()
			edges.appoint_unit_edges_costs(field)

		heuristic_value = dict() # heuristic function from A* algorithm
		for cell in field.get_board():
			heuristic_value[cell] = field.calculate_heuristic_value(cell, goal)

		priority_queue = heapdict() # priority queue of cells from A* algorithm
		priority_queue[start] = heuristic_value[start]

		start.distance = 0
		distance = dict() # distance from start cell to current
		for cell in field.get_board():
			distance[cell] = INFINITY
		distance[start] = 0

		predecessor = dict() # previous cell on the path from the start cell to current
		for cell in field.get_board():
			predecessor[cell] = None
		predecessor[start] = start

		while len(priority_queue) != 0:
			current_cell, _ = priority_queue.popitem()
		
			for next_cell, edge_cost in edges.get_neigbours(current_cell):
				new_distance = distance[current_cell] + edge_cost
				if new_distance < distance[next_cell]:
					distance[next_cell] = new_distance
					predecessor[next_cell] = current_cell
					priority_queue[next_cell] = distance[next_cell] + heuristic_value[next_cell]
		
		if distance[goal] == INFINITY: # goal cell is unreachable
			return (None, None)

		cell_on_the_path = goal # path recovery
		path = []
		while predecessor[cell_on_the_path] != cell_on_the_path:
			path.append(cell_on_the_path)
			cell_on_the_path = predecessor[cell_on_the_path]
		path.append(cell_on_the_path)


		return (distance[goal], path[::-1])