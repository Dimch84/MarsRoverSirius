import unittest
from textwrap import dedent

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '../src'))

from a_star import A_star
from lifelong_a_star import Lifelong_a_star
from testing_stuff import is_path_correct 

class Test_offline_algorithms(unittest.TestCase):
	"""
	This class check the work correctness of A* and longlife A* algorithms implementations
	"""
	functions = [A_star.call, Lifelong_a_star.call] 
	def test_path_length_with_unlock_field(self):
		field = dedent('''\
			00000
			00000
			00000
			00000
			00000''').split('\n')

		for test_function in self.functions:
			self.assertEqual(test_function(start=(0, 0), goal=(4, 4), field=field)[0], 4)
			self.assertEqual(test_function(start=(0, 0), goal=(0, 4), field=field)[0], 4)
			self.assertEqual(test_function(start=(2, 2), goal=(0, 4), field=field)[0], 2)
			self.assertEqual(test_function(start=(1, 4), goal=(4, 0), field=field)[0], 4)
			self.assertEqual(test_function(start=(1, 2), goal=(1, 4), field=field)[0], 2)
			self.assertEqual(test_function(start=(3, 2), goal=(3, 2), field=field)[0], 0)
			self.assertEqual(test_function(start=(4, 3), goal=(3, 4), field=field)[0], 1)

	def test_path_length_with_lock_cells(self):
		field = dedent('''\
			00000
			00100
			01110
			00100
			00000''').split('\n')

		for test_function in self.functions:
			self.assertEqual(test_function(start=(0, 0), goal=(4, 4), field=field)[0], 6)
			self.assertEqual(test_function(start=(0, 0), goal=(3, 3), field=field)[0], 5)
			self.assertEqual(test_function(start=(1, 1), goal=(3, 3), field=field)[0], 4)
			self.assertEqual(test_function(start=(2, 0), goal=(2, 4), field=field)[0], 4)
			self.assertEqual(test_function(start=(1, 4), goal=(3, 1), field=field)[0], 4)
			self.assertEqual(test_function(start=(1, 1), goal=(2, 4), field=field)[0], 3)
			self.assertEqual(test_function(start=(4, 0), goal=(4, 4), field=field)[0], 4)

	def test_path_recovery(self):
		field = dedent('''\
			00000
			00100
			01110
			00100
			00100''').split('\n')

		start_1 = (0, 0)
		goal_1 = (4, 4)
		for test_function in self.functions:
			path_length_1, path_1 = test_function(start=start_1, goal=goal_1, field=field)
			self.assertEqual(path_length_1, 6)
			self.assertTrue(is_path_correct(field, start_1, goal_1, path_1, path_length_1))

		start_2 = (4, 1)
		goal_2 = (4, 3)
		for test_function in self.functions:
			path_length_2, path_2 = test_function(start=start_2, goal=goal_2, field=field)
			self.assertEqual(path_length_2, 8)
			self.assertTrue(is_path_correct(field, start_2, goal_2, path_2, path_length_2))

	def test_lack_of_the_path(self):
		field = dedent('''\
			00100
			00100
			01111
			00100
			00100''').split('\n')

		for test_function in self.functions:
			self.assertEqual(test_function(start=(0, 0), goal=(4, 4), field=field), (None, None))
			self.assertEqual(test_function(start=(1, 3), goal=(2, 0), field=field), (None, None))
			self.assertEqual(test_function(start=(1, 1), goal=(4, 1), field=field)[0], 3)
			self.assertEqual(test_function(start=(0, 4), goal=(3, 3), field=field), (None, None))

	def test_with_weighted_edges(self):
		field = dedent('''\
			000
			010
			000''').split('\n')

		edges_dict = {((0, 0), (0, 1)) : 1,
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

		for test_function in self.functions:
			self.assertEqual(test_function(start=(0, 0), goal=(2, 2), field=field, edges_dict=edges_dict)[0], 8)
			self.assertEqual(test_function(start=(1, 0), goal=(2, 1), field=field, edges_dict=edges_dict)[0], 3)
			self.assertEqual(test_function(start=(1, 0), goal=(1, 2), field=field, edges_dict=edges_dict)[0], 5)
			self.assertEqual(test_function(start=(2, 0), goal=(0, 2), field=field, edges_dict=edges_dict)[0], 4)

			