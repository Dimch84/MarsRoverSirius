import numpy as np

from a_star import A_star

INFINITY = 1000

def genererate_masks(size: int) -> [int]:
	masks = []
	for mask in range(1 << size):
		cnt = 0
		for i in range(size):
			if mask & (1 << i):
				cnt += 1
		masks.append((mask, cnt))
	sorted(masks)
	return list(map(lambda item: item[0], masks[1:]))

def get_neigbours(mask: int, size: int) -> [(int, int)]:
	neigbour_masks = []
	for i in range(size):
		if mask & (1 << i):
			neigbour_masks.append((mask ^ (1 << i), i))
	return neigbour_masks

class Intermediate_points_algorithm:
	@staticmethod
	def call(start: (int, int),
			 goal: (int, int),
			 intermidiate_points: [(int, int)],
			 field: [str],
			 edges_dict: dict = None) -> (int, [(int, int)]):
		intermidiate_points_number = len(intermidiate_points)
		points_mask = genererate_masks(intermidiate_points_number)
		ans = [[INFINITY] * intermidiate_points_number for _ in range(len(points_mask) + 1)]
		previous_point = [list(np.arange(0, intermidiate_points_number)) for _ in range(len(points_mask) + 1)]
		for current_mask in points_mask:
			for neigbour_mask, end_point_number in get_neigbours(current_mask, intermidiate_points_number):
				if neigbour_mask == 0:
					path_cost, path = A_star.call(start=start, goal=intermidiate_points[end_point_number], field=field)
					ans[current_mask][end_point_number] = path_cost
					previous_point[current_mask][end_point_number] = -1
					continue
				for last_point_number in range(intermidiate_points_number):
					if neigbour_mask & (1 << last_point_number) == 0:
						continue
					path_cost, path = A_star.call(start=intermidiate_points[last_point_number], goal=intermidiate_points[end_point_number], field=field)
					if ans[neigbour_mask][last_point_number] + path_cost < ans[current_mask][end_point_number]:
						ans[current_mask][end_point_number] = ans[neigbour_mask][last_point_number] + path_cost
						previous_point[current_mask][end_point_number] = last_point_number
		summary_cost, goals_previous_point = INFINITY, None
		for last_point_number in range(intermidiate_points_number):
			path_cost, path = A_star.call(start=intermidiate_points[last_point_number], goal=goal, field=field)
			if ans[points_mask[-1]][last_point_number] + path_cost < summary_cost:
				summary_cost = ans[points_mask[-1]][last_point_number] + path_cost
				goals_previous_point = last_point_number
		
		# path recovering 
		_, path = A_star.call(start=intermidiate_points[goals_previous_point], goal=goal, field=field)
		answer_path = path
		current_mask, current_point = points_mask[-1], goals_previous_point
		while previous_point[current_mask][current_point] != -1:
			last_point = previous_point[current_mask][current_point]
			_, path = A_star.call(start=intermidiate_points[last_point], goal=intermidiate_points[current_point], field=field)
			answer_path = path[:-1] + answer_path
			current_mask = current_mask ^ (1 << current_point)
			current_point = last_point
		answer_path.reverse()

		return summary_cost, answer_path
