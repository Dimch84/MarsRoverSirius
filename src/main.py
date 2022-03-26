from a_star import A_star
from field import Field

def main():
	height, width = list(map(int, input().split()))
	field_input = [input() for i in range(height)]
	start = tuple(list(map(int, input().split())))
	goal = tuple(list(map(int, input().split())))
	answer, path = A_star.call(start, goal, field_input)
	print(answer)
	print(path)

if __name__ == "__main__":
	main()