from enum import Enum
from itertools import product
from random import random, randrange
from tkinter import BOTH, Canvas, Event, Frame


class SquareType(Enum):
    FREE = 0
    BLOCKED = 1
    START = 2
    FINISH = 3


class Map(Frame):
    """
    This class provides methods for generating a map and drawing it on the screen.
    :param width: the width of the map in squares.
    :param height: the height of the map in squares.
    :param density: the likelihood of a square to be blocked.
    """
    padding = 10
    square_size = 50
    start_position = (0, 0)
    finish_position = (0, 0)
    alt_pressed = False
    shift_pressed = False

    def __init__(self, width: int = 10, height: int = 10,
                 density: float = 0.5) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.density = density
        self.map = [[SquareType.FREE for _ in range(width)]
                    for _ in range(height)]
        self.canvas = Canvas(self)
        self.add_binds()
        self.generate_random()

    def add_binds(self) -> None:
        """
        This function adds binds to process user input.
        :return:
        """
        self.canvas.bind('<Button>', self.change_square)
        self.focus_set()
        self.bind('<KeyPress>', self.process_key_press)
        self.bind('<KeyRelease>', self.process_key_release)

    def process_key_press(self, event: Event) -> None:
        """
        This function processes a key press event, it should be used in widget.bind.
        :param event: tkinter event.
        :return:
        """
        key = event.keysym
        if key == 'Alt_L' or key == 'Alt_R':
            self.alt_pressed = True
        elif key == 'Shift_L' or key == 'Shift_R':
            self.shift_pressed = True

    def process_key_release(self, event: Event) -> None:
        """
        This function processes a key release event, it should be used in widget.bind.
        :param event: tkinter event.
        :return:
        """
        key = event.keysym
        if key == 'Alt_L' or key == 'Alt_R':
            self.alt_pressed = False
        elif key == 'Shift_L' or key == 'Shift_R':
            self.shift_pressed = False

    def generate_random(self) -> None:
        """
        This method randomly fills the map.
        :return:
        """
        self.map = [[SquareType.FREE for _ in range(self.width)]
                    for _ in range(self.height)]
        for i, j in product(range(self.height), range(self.width)):
            if random() < self.density:
                self.map[i][j] = SquareType.BLOCKED
        start_row = randrange(self.height)
        start_col = randrange(self.width)
        self.start_position = (start_row, start_col)
        self.map[start_row][start_col] = SquareType.START
        finish_row = randrange(self.height)
        finish_col = randrange(self.width)
        self.finish_position = (finish_row, finish_col)
        self.map[finish_row][finish_col] = SquareType.FINISH

    def draw(self) -> None:
        """
        This method draws the map.
        :return:
        """
        self.pack(fill=BOTH, expand=1)
        for i, j in product(range(self.height), range(self.width)):
            self.draw_square(i, j)
        self.canvas.pack(fill=BOTH, expand=1)

    def change_square(self, event: Event) -> None:
        """
        This method changes a square on mouse click, it should be used in widget.bind.
        :param event: tkinter event.
        :return:
        """
        row_index = (event.y - self.padding) // self.square_size
        col_index = (event.x - self.padding) // self.square_size
        if row_index < 0 or row_index >= self.height:
            return
        if col_index < 0 or col_index >= self.width:
            return
        if self.alt_pressed:
            self.change_special_square(row_index, col_index, SquareType.START)
        elif self.shift_pressed:
            self.change_special_square(row_index, col_index, SquareType.FINISH)
        else:
            self.change_normal_square(row_index, col_index)

    def change_normal_square(self, row_index: int, col_index: int) -> None:
        """
        This function changes a square from free to blocked and vice versa.
        :param row_index: row index.
        :param col_index: column index.
        :return:
        """
        if self.map[row_index][col_index] == SquareType.BLOCKED:
            self.map[row_index][col_index] = SquareType.FREE
        elif self.map[row_index][col_index] == SquareType.FREE:
            self.map[row_index][col_index] = SquareType.BLOCKED
        self.draw_square(row_index, col_index)

    def change_special_square(self, row_index: int, col_index: int,
                              square_type: SquareType) -> None:
        """
        This function changes the position of the start or the finish.
        :param row_index: new row index.
        :param col_index: new column index.
        :param square_type: start or finish.
        :return:
        """
        if self.map[row_index][col_index] == square_type:
            return
        if square_type == SquareType.START:
            old_row = self.start_position[0]
            old_col = self.start_position[1]
            self.start_position = (row_index, col_index)
        elif square_type == SquareType.FINISH:
            old_row = self.finish_position[0]
            old_col = self.finish_position[1]
            self.finish_position = (row_index, col_index)
        else:
            return
        self.map[old_row][old_col] = SquareType.FREE
        self.map[self.start_position[0]][self.start_position[1]] \
            = SquareType.START
        self.map[self.finish_position[0]][self.finish_position[1]] \
            = SquareType.FINISH
        self.draw_square(old_row, old_col)
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
        square_type = self.map[row_index][col_index]
        color = 'white'
        if square_type == SquareType.FREE:
            color = 'green'
        elif square_type == SquareType.BLOCKED:
            color = 'red'
        elif square_type == SquareType.START:
            color = 'blue'
        elif square_type == SquareType.FINISH:
            color = 'yellow'
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
