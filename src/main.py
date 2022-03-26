from A_star import A_star

def main():
	height, width = list(map(int, input().split()))
	field_input = [input() for i in range(height)]
	field = dict()
	for i in range(height):
		for j in range(width):
			field[(i, j)] = field_input[i][j]
	start = tuple(list(map(int, input().split())))
	goal = tuple(list(map(int, input().split())))
	answer, path = A_star.get_optimal_path(start, goal, field)
	print(answer)
	print(path)

if __name__ == "__main__":
	main()