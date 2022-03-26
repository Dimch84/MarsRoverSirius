import unittest
from textwrap import dedent

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '../src'))

from A_star import A_star

def build_field(field_input: str, height: int, width: int) -> dict:
	"""
	This method transform string cell field into dictionary cell field
	param field_input: string field of cells
	param height: field height
	param width: field width 
	"""
	field = dict()
	for i in range(height):
		for j in range(width):
			field[(i, j)] = field_input[i * (width + 1) + j]
	return field

def is_path_correct(field: dict, start: (int, int), goal: (int, int), path: (int, int), correct_path_length: (int, int)) -> bool:
	"""
	This method check correctness and optimality of the path from start cell to goal cell
	param field: dictionary of cells with blocking information:
	    '0' - cell is unlock
	    '1' - cell is lock
	param start: start cell
	param goal: goal cell
	param path: proposed path
	param correct_path_length: correct path length 
	"""

	if len(path) != correct_path_length + 1:
		return False

	cell_is_correct = (lambda cell : cell in field.keys() and field[cell] == '0')
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


class Test(unittest.TestCase):
	"""
	This class check the work of A* algorithm implementation
	"""
	def test_path_length_with_unlock_field(self):
		height, width = 5, 5
		field_input = dedent('''\
			00000
			00000
			00000
			00000
			00000''')

		field = build_field(field_input, height, width)
		
		self.assertEqual(A_star.get_optimal_path(start=(0, 0), goal=(4, 4), field=field)[0], 4)
		self.assertEqual(A_star.get_optimal_path(start=(0, 0), goal=(0, 4), field=field)[0], 4)
		self.assertEqual(A_star.get_optimal_path(start=(2, 2), goal=(0, 4), field=field)[0], 2)
		self.assertEqual(A_star.get_optimal_path(start=(1, 4), goal=(4, 0), field=field)[0], 4)
		self.assertEqual(A_star.get_optimal_path(start=(1, 2), goal=(1, 4), field=field)[0], 2)
		self.assertEqual(A_star.get_optimal_path(start=(3, 2), goal=(3, 2), field=field)[0], 0)
		self.assertEqual(A_star.get_optimal_path(start=(4, 3), goal=(3, 4), field=field)[0], 1)

	def test_path_length_with_lock_cells(self):
		height, width = 5, 5
		field_input = dedent('''\
			00000
			00100
			01110
			00100
			00000''')

		field = build_field(field_input, height, width)
		
		self.assertEqual(A_star.get_optimal_path(start=(0, 0), goal=(4, 4), field=field)[0], 6)
		self.assertEqual(A_star.get_optimal_path(start=(0, 0), goal=(3, 3), field=field)[0], 5)
		self.assertEqual(A_star.get_optimal_path(start=(1, 1), goal=(3, 3), field=field)[0], 4)
		self.assertEqual(A_star.get_optimal_path(start=(2, 0), goal=(2, 4), field=field)[0], 4)
		self.assertEqual(A_star.get_optimal_path(start=(1, 4), goal=(3, 1), field=field)[0], 4)
		self.assertEqual(A_star.get_optimal_path(start=(1, 1), goal=(2, 4), field=field)[0], 3)
		self.assertEqual(A_star.get_optimal_path(start=(4, 0), goal=(4, 4), field=field)[0], 4)

	def test_path_recovery(self):
		height, width = 5, 5
		field_input = dedent('''\
			00000
			00100
			01110
			00100
			00100''')

		field = build_field(field_input, height, width)

		start_1 = (0, 0)
		goal_1 = (4, 4)
		path_length_1, path_1 = A_star.get_optimal_path(start=start_1, goal=goal_1, field=field)
		self.assertEqual(path_length_1, 6)
		self.assertEqual(is_path_correct(field, start_1, goal_1, path_1, path_length_1), True)

		start_2 = (4, 1)
		goal_2 = (4, 3)
		path_length_2, path_2 = A_star.get_optimal_path(start=start_2, goal=goal_2, field=field)
		self.assertEqual(path_length_2, 8)
		self.assertEqual(is_path_correct(field, start_2, goal_2, path_2, path_length_2), True)

	def test_lack_of_the_path(self):
		height, width = 5, 5
		field_input = dedent('''\
			00100
			00100
			01111
			00100
			00100''')

		field = build_field(field_input, height, width)

		self.assertEqual(A_star.get_optimal_path(start=(0, 0), goal=(4, 4), field=field), (None, None))
		self.assertEqual(A_star.get_optimal_path(start=(1, 3), goal=(2, 0), field=field), (None, None))
		self.assertEqual(A_star.get_optimal_path(start=(1, 1), goal=(4, 1), field=field)[0], 3)
		self.assertEqual(A_star.get_optimal_path(start=(0, 4), goal=(3, 3), field=field), (None, None))

	def test_with_weighted_edges(self):
		height, width = 3, 3
		field_input = dedent('''\
			000
			010
			000''')

		field = build_field(field_input, height, width)
		edges_cost = {((0, 0), (0, 1)) : 1,
		              ((0, 0), (1, 0)) : 2,
		              ((0, 1), (0, 2)) : 3,
		              ((0, 1), (1, 2)) : 4,
		              ((0, 1), (1, 0)) : 2,
		              ((0, 2), (1, 2)) : 1,
		              ((1, 0), (2, 0)) : 2,
		              ((1, 0), (2, 1)) : 4,
		              ((1, 2), (2, 1)) : 2,
		              ((1, 2), (2, 2)) : 4,
		              ((2, 0), (2, 1)) : 1,
		              ((2, 1), (2, 2)) : 3}

		self.assertEqual(A_star.get_optimal_path(start=(0, 0), goal=(2, 2), field=field, edges_cost=edges_cost)[0], 8)
		self.assertEqual(A_star.get_optimal_path(start=(1, 0), goal=(2, 1), field=field, edges_cost=edges_cost)[0], 3)
		self.assertEqual(A_star.get_optimal_path(start=(1, 0), goal=(1, 2), field=field, edges_cost=edges_cost)[0], 5)
		self.assertEqual(A_star.get_optimal_path(start=(2, 0), goal=(0, 2), field=field, edges_cost=edges_cost)[0], 4)
		


