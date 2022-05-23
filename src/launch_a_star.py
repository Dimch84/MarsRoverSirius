import sys 
from json import dump, load

from src.a_star import *

# file_out = sys.argv[1]
# n = int(sys.argv[2])
# m = int(sys.argv[3])
# start = (int(sys.argv[4]), int(sys.argv[5]))
# goal = (int(sys.argv[6]), int(sys.argv[7]))
#
#
# field = []
# for i in range(n):
#     field_i = []
#     for j in range(m):
#         field_i.append(int(sys.argv[8 + i*n + j]))
#     field.append(field_i)


def get_direction_path(path: [(int, int)]) -> [(int, int)]:
    direction_path = []
    for i in range(len(path[:-1])):
         current_cell, next_cell = path[i], path[i + 1]
         direction_path.append((next_cell[0] - current_cell[0], next_cell[1] - current_cell[1]))
    return direction_path


def f(array: [[int]]):
    string_array = []
    for subarray in array:
        string_array.append(''.join(map(str,subarray)))
    return string_array

# path_length, path = A_star.call(start, goal, f(field))
# direction_path = get_direction_path(path)
#
#
#
# field_data = {
#             'path': direction_path
#         }
# with open(file_out, 'w') as file:
#     dump(field_data, file, indent=2)