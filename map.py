from itertools import product
from random import random
from tkinter import BOTH, Canvas, Frame


class Map(Frame):
    """
    This class provides methods for generating a map and drawing it on screen.
    :param width: the width of the map in squares.
    :param height: the height of the map in squares.
    :param density: the likelihood of a square to be filled.
    """
    padding = 10
    square_size = 50

    def __init__(self, width: int = 10, height: int = 10, density: float = 0.5) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.density = density
        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.generate_random()

    def generate_random(self) -> None:
        """
        This method fills the map with random values.
        """
        for i, j in product(range(self.height), range(self.width)):
            if random() < self.density:
                self.map[i][j] = 1

    def draw(self) -> None:
        """
        This method creates a canvas and draws the map on it.
        """
        canvas = Canvas(self)
        self.pack(fill=BOTH, expand=1)
        for i, j in product(range(self.height), range(self.width)):
            x0 = self.padding + j * self.square_size
            x1 = x0 + self.square_size
            y0 = self.padding + i * self.square_size
            y1 = y0 + self.square_size
            if self.map[i][j]:
                canvas.create_rectangle(x0, y0, x1, y1, fill='red')
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill='green')
        canvas.pack(fill=BOTH, expand=1)
