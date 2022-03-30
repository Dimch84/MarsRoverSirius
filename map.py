from itertools import product
from random import random
from tkinter import BOTH, Canvas, Event, Frame


class Map(Frame):
    """
    This class provides methods for generating a map and drawing it on screen.
    :param width: the width of the map in squares.
    :param height: the height of the map in squares.
    :param density: the likelihood of a square to be filled.
    """
    padding = 10
    square_size = 50

    def __init__(self, width: int = 10, height: int = 10,
                 density: float = 0.5) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.density = density
        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.canvas = Canvas(self)
        self.generate_random()

    def generate_random(self) -> None:
        """
        This method fills the map with random values.
        :return:
        """
        for i, j in product(range(self.height), range(self.width)):
            if random() < self.density:
                self.map[i][j] = 1

    def draw(self) -> None:
        """
        This method creates a canvas and draws the map on it.
        :return:
        """
        self.pack(fill=BOTH, expand=1)
        for i, j in product(range(self.height), range(self.width)):
            self.draw_square(i, j)
        self.canvas.pack(fill=BOTH, expand=1)

    def change_square(self, event: Event) -> None:
        """
        This method changes square on mouse click, it should be used in widget.bind.
        :param event: tkinter event.
        :return:
        """
        row_index = (event.y - self.padding) // self.square_size
        col_index = (event.x - self.padding) // self.square_size
        if row_index < 0 or row_index >= self.height:
            return
        if col_index < 0 or col_index >= self.width:
            return
        self.map[row_index][col_index] = not self.map[row_index][col_index]
        self.draw_square(row_index, col_index)

    def draw_square(self, row_index: int, col_index: int) -> None:
        """
        This method draws a square at given coordinates.
        :param row_index: row index.
        :param col_index: column index.
        :return:
        """
        x0 = self.padding + col_index * self.square_size
        x1 = x0 + self.square_size
        y0 = self.padding + row_index * self.square_size
        y1 = y0 + self.square_size
        if self.map[row_index][col_index]:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='red')
        else:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='green')
