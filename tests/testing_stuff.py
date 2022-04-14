def is_path_correct(field: [str], 
	                start: (int, int), 
	                goal: (int, int), 
	                path: [(int, int)], 
	                correct_path_length: int = -1) -> bool:
	"""
	This method check correctness and optimality of the path from start cell to goal cell
	param field: matrix of cells with blocking information:
	    '0' - cell is unlock
	    '1' - cell is lock
	param start: start cell coordinates
	param goal: goal cell coordinates
	param path: given path of cells coordinates
	param correct_path_length: correct path length 
	"""

	if correct_path_length != -1 and len(path) != correct_path_length + 1:
		return False

	height, width = len(field), len(field[0])

	cell_is_correct = (lambda cell : 0 <= cell[0] < height and 0 <= cell[1] < width and field[cell[0]][cell[1]] == '0')
	cells_are_neigbours = (lambda cell_1, cell_2 : abs(cell_1[0] - cell_2[0]) <= 1 and abs(cell_1[1] - cell_2[1]) <= 1)
	
	for i, cell in enumerate(path):
		if cell_is_correct(cell) == False:
			return False
		if i == 0:
			if cell != start:
				return False
		else:
			if cells_are_neigbours(cell, path[i - 1]) == False:
				return False
	return path[-1] == goal