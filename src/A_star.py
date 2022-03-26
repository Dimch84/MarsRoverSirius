from heapdict import heapdict

STEPS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
INFINITY = 1000

def get_neigbours(field: dict, cell: (int, int)) -> [(int, int)]:
	"""
	This method returns all available neigbours of current cell
	param field: dictionary of cells with blocking information:
	    '0' - cell is unlock
	    '1' - cell is lock
	param cell: current cell
	"""
	potential_neighbours = [(delta_x + cell[0], delta_y + cell[1]) 
		for delta_x, delta_y in STEPS]
	return filter(lambda cell : cell in field.keys() and field[cell] == '0', potential_neighbours)

def get_unit_edges_costs(field: dict) -> dict:
	"""
	This method appoints all edges unit cost
	param field: dictionary of cells with blocking information:
	    '0' - cell is unlock
	    '1' - cell is lock
	"""
	
	edges_cost = dict()
	for cell in field:
		for neigbour_cell in get_neigbours(field, cell):
			edges_cost[(min(cell, neigbour_cell), max(cell, neigbour_cell))] = 1
	return edges_cost



class A_star(object):
	@staticmethod
	def get_optimal_path(start: (int, int), 
		                 goal: (int, int), 
		                 field: dict,
		                 edges_cost: dict = None) -> (int, [(int, int)]):
		"""
		This method calculates path (and his length) from start cell to goal cell with A* algorithm
		param start: start cell
		param goal: goal cell
		param field: dictionary of cells with blocking information:
		    '0' - cell is unlock
		    '1' - cell is lock
		param edges_cost: dictionary of edges with their cost 
		"""

		if edges_cost == None: # if edges_cost wasn't passed to method then every edge has unit cost
			edges_cost = get_unit_edges_costs(field)
		
		heuristic_value = dict() # heuristic function from A* algorithm
		for cell in field:
			heuristic_value[cell] = max(abs(start[0] - cell[0]), abs(start[1] - cell[1]))

		priority_queue = heapdict() # priority queue of cells from A* algorithm
		priority_queue[start] = heuristic_value[start]

		distance = dict() # distance from start cell to current
		for cell in field:
			distance[cell] = INFINITY
		distance[start] = 0

		predecessor = dict() # previous cell on the path from the start cell to current
		for cell in field:
			predecessor[cell] = None
		predecessor[start] = start

		get_edge_cost = (lambda cell_1, cell_2 : edges_cost[(min(cell_1, cell_2), max(cell_1, cell_2))])	

		while len(priority_queue) != 0:
			current_cell, _ = priority_queue.popitem()

			for next_cell in get_neigbours(field, current_cell):
				edge_cost = get_edge_cost(current_cell, next_cell)
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
