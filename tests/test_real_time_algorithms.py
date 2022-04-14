import unittest
from textwrap import dedent
from collections.abc import Callable

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '../src'))

from real_time_algorithm import Real_time_algorithm
from testing_stuff import is_path_correct


class Test_real_time_algorithms(unittest.TestCase):
	"""
	This class check the work correctness of RTAA* algorithm implementation
	"""
	functions = [Real_time_algorithm.call]
	def get_message(self, start: (int, int), goal: (int, int), is_path_exsists: bool = True) -> str:
		if is_path_exsists:
			return "Given path from start cell: " + str(start) + " to goal cell: " + str(goal) + " is incorrect!"
		return "There is should be no path from start cell: " + str(start) + " to goal cell: " + str(goal)


	def check_tests(self,
			        field: [[str]], 
		            end_cells: [((int, int), (int, int))],
		            is_correct_path_exists: bool = True,
		            expansions_limits: range = range(2, 10)):
		for test_function in self.functions:
			for start, goal in end_cells:
				for expansions_limit in expansions_limits:
					path = test_function(start=start, goal=goal, field=field, expansions_limit=expansions_limit)
					if is_correct_path_exists == True:
						self.assertTrue(is_path_correct(field, start, goal, path), msg=self.get_message(start, goal))
					else:
						self.assertEqual(path, None, msg=self.get_message(start, goal, is_path_exsists=False))

	def test_path_correctness_with_unlock_field(self):
		field = dedent('''\
			00000
			00000
			00000
			00000
			00000''').split('\n')
		end_cells = [((0, 0), (4, 4)),
		             ((1, 1), (3, 3)),
		             ((3, 1), (2, 3)),
		             ((0, 4), (4, 0))]
		self.check_tests(field, end_cells)


	def test_path_correctness_with_lock_cells(self):
		field = dedent('''\
			01000
			01010
			01010
			01010
			00010''').split('\n')
		end_cells = [((0, 0), (4, 4)),
			         ((0, 0), (0, 2)),
			         ((3, 0), (3, 2)),
			         ((4, 0), (0, 4))]
		self.check_tests(field, end_cells)


	def test_lack_of_the_path(self):
		field = dedent('''\
			01000
			00100
			11111
			00000
			00100''').split('\n')
		end_cells_with_exsisting_path = [((0, 0), (1, 1)),
			         					 ((0, 0), (1, 4)),
			                             ((3, 0), (4, 4)),
			                             ((4, 1), (4, 4))]
		self.check_tests(field, end_cells_with_exsisting_path)
		end_cells_with_lack_of_the_path = [((0, 0), (4, 4)),
		 	         					   ((0, 0), (4, 0)),
		 	                               ((1, 3), (3, 0)),
		 	                               ((1, 0), (4, 4))]
		self.check_tests(field, end_cells_with_lack_of_the_path, is_correct_path_exists=False)
					