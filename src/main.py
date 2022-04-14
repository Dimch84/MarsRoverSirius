from textwrap import dedent

from a_star import A_star 
from a_star import Path_planning_algorithm
from lifelong_a_star import Lifelong_a_star
from real_time_algorithm import Real_time_algorithm
from field import Field

def main():
	# height, width = list(map(int, input().split()))
	# field_input = [input() for i in range(height)]
	# start = tuple(list(map(int, input().split())))
	# goal = tuple(list(map(int, input().split())))
	# answer, path = Lifelong_a_star.call(start, goal, field_input)
	# print(answer)
	# print(path)

	field_input = dedent('''\
			01000
			01010
			01010
			01010
			00010''').split('\n')
	start, goal = (0, 0), (4, 4)

	# height, width = list(map(int, input().split()))
	# field_input = [input() for i in range(height)]
	# start = tuple(list(map(int, input().split())))
	# goal = tuple(list(map(int, input().split())))
	path = Real_time_algorithm.call(start=start, goal=goal, field=field_input, expansions_limit=5)
	print(path)


if __name__ == "__main__":
	main()


