from enum import IntEnum
from itertools import product
from os.path import exists
from random import random, randrange
from tkinter import BOTH, Canvas, Event, Frame, TOP


class SquareType(IntEnum):
    FREE = 0
    BLOCKED = 1
    START = 2
    FINISH = 3


SquareTypeColor = {
    SquareType.FREE: 'green',
    SquareType.BLOCKED: 'red',
    SquareType.START: 'blue',
    SquareType.FINISH: 'yellow'
}


class Square:
    """
    This class contains information about one square on the canvas and provides methods to change its parameters.

    :param canvas: the canvas on which to draw the square.
    :param square_type: the type of the square.
    :param size: the size of the square.
    :param position: the position of the top left corner of the square.
    :param square_id: the id of the square on the canvas.
    """
    def __init__(
            self, canvas: Canvas, square_type: SquareType = SquareType.FREE,
            size: int = 0, position: tuple = (0, 0), square_id: int = None):
        self.__canvas = canvas
        self.square_type = square_type
        self.position = position
        self.size = size
        self.__square_id = square_id

    def draw(self, size: int = None, position: tuple = None) -> None:
        """
        This method changes the size and the position of this square and draws it on the canvas.

        :param size: new size of the square.
        :param position: new position of the square.
        :return:
        """
        if size is not None:
            self.size = size
        if position is not None:
            self.position = position
        if self.__square_id is None:
            self.__create()
        else:
            x0, y0, x1, y1 = self.get_coordinates()
            self.__canvas.coords(self.__square_id, x0, y0, x1, y1)

    def change_type(self, square_type: SquareType) -> None:
        """
        This method changes the type of this square.

        :param square_type: new type of the square.
        :return:
        """
        self.square_type = square_type
        if self.__square_id is None:
            self.__create()
        else:
            self.__canvas.itemconfig(self.__square_id,
                                     fill=SquareTypeColor[self.square_type])

    def get_coordinates(self) -> tuple:
        """
        This method returns the position of the top left and bottom right corners of this square.

        :return: 4 coordinates.
        """
        return (self.position[0], self.position[1],
                self.position[0] + self.size, self.position[1] + self.size)

    def __create(self) -> None:
        """
        This method creates a new square on the canvas.

        :return:
        """
        x0, y0, x1, y1 = self.get_coordinates()
        self.__square_id = self.__canvas.create_rectangle(
            x0, y0, x1, y1, fill=SquareTypeColor[self.square_type])


class Field(Frame):
    """
    This class provides methods for generating a field and drawing it on the screen.

    :param width: the width of the field in squares.
    :param height: the height of the field in squares.
    :param density: the likelihood of a square to be blocked.
    """
    __padding = 5
    __square_size = 128
    __max_square_size = 256
    __min_square_size = 2
    __scale_coefficient = 2
    __scale_level = __max_square_size // __square_size
    __start_position = (0, 0)
    __finish_position = (0, 0)
    __alt_pressed = False
    __shift_pressed = False

    def __init__(self, width: int = 10, height: int = 10,
                 density: float = 0.5) -> None:
        super().__init__()
        self.__width = width
        self.__height = height
        self.__density = density
        self.__field_data = []
        self.__canvas = Canvas(self)
        self.pack(fill=BOTH, side=TOP, expand=1)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__add_binds()
        self.reset()

    def generate_random(self) -> None:
        """
        This method randomly fills the field.

        :return:
        """
        self.reset()
        for row, col in product(range(self.__height), range(self.__width)):
            if random() < self.__density:
                self.__field_data[row][col].change_type(SquareType.BLOCKED)
        start_row = randrange(self.__height)
        start_col = randrange(self.__width)
        self.__start_position = (start_row, start_col)
        self.__field_data[start_row][start_col]. \
            change_type(SquareType.START)
        finish_row = randrange(self.__height)
        finish_col = randrange(self.__width)
        self.__finish_position = (finish_row, finish_col)
        self.__field_data[finish_row][finish_col]. \
            change_type(SquareType.FINISH)

    def save(self, file_name: str) -> None:
        """
        This method saves the field to a text file.

        :param file_name: output file name.
        :return:
        """
        with open(file_name, 'w') as file:
            file.write(f'{self.__width} {self.__height}\n')
            for row in range(self.__height):
                for col in range(self.__width):
                    square_type = self.__field_data[row][col].square_type
                    file.write(f'{int(square_type)} ')
                file.write('\n')
            file.write(f'{self.__start_position[0]} '
                       f'{self.__start_position[1]}\n')
            file.write(f'{self.__finish_position[0]} '
                       f'{self.__finish_position[1]}\n')

    def load(self, file_name: str) -> None:
        """
        This method loads the field from a text file.

        :param file_name: input file name.
        :return:
        """
        if not exists(file_name):
            print(f'Could not load "{file_name}", file does not exist.')
            return
        with open(file_name, 'r') as file:
            self.__width, self.__height = map(int, file.readline().split())
            self.reset()
            for row in range(self.__height):
                square_types = list(map(lambda x: SquareType(int(x)),
                                        file.readline().split()))
                for col in range(self.__width):
                    self.__field_data[row][col].change_type(square_types[col])
            self.__start_position = tuple(map(int, file.readline().split()))
            self.__finish_position = tuple(map(int, file.readline().split()))

    def reset(self) -> None:
        """
        This method fills the field with free squares and sets start and finish at (0,0).

        :return:
        """
        self.__canvas.delete('all')
        self.__field_data = [[Square(self.__canvas, size=self.__square_size)
                             for _ in range(self.__width)]
                             for _ in range(self.__height)]
        self.__start_position = (0, 0)
        self.__finish_position = (0, 0)
        self.__field_data[0][0].change_type(SquareType.FINISH)
        self.__draw()

    def get_frame_width(self) -> int:
        """
        This method returns the width of the field on the screen.

        :return: field frame width.
        """
        self.update()
        return self.winfo_width()

    def get_frame_height(self) -> int:
        """
        This method returns the height of the field on the screen.

        :return: field frame height.
        """
        self.update()
        return self.winfo_height()

    def __draw(self) -> None:
        """
        This method draws the field.

        :return:
        """
        for row, col in product(range(self.__height),
                                range(self.__width)):
            self.__draw_square(row, col)

    def __add_binds(self) -> None:
        """
        This method adds binds to this class to process user input.

        :return:
        """
        self.__canvas.bind('<Button>', self.__change_square)
        self.focus_set()
        self.bind('<KeyPress>', self.__process_key_press)
        self.bind('<KeyRelease>', self.__process_key_release)

    def __process_key_press(self, event: Event) -> None:
        """
        This method processes a key press event, it should be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        key = event.keysym
        if key == 'Alt_L' or key == 'Alt_R':
            self.__alt_pressed = True
        elif key == 'Shift_L' or key == 'Shift_R':
            self.__shift_pressed = True
        elif key == 'plus':
            self.__zoom_in()
        elif key == 'minus':
            self.__zoom_out()
        elif key == 'Right':
            self.__move_right()
        elif key == 'Left':
            self.__move_left()
        elif key == 'Down':
            self.__move_down()
        elif key == 'Up':
            self.__move_up()

    def __zoom_in(self) -> None:
        """
        This method zooms in the field.

        :return:
        """
        if self.__square_size >= self.__max_square_size:
            return
        self.__square_size *= self.__scale_coefficient
        self.__scale_level //= self.__scale_coefficient
        self.__canvas.scale('all', self.__padding, self.__padding,
                            self.__scale_coefficient,
                            self.__scale_coefficient)

    def __zoom_out(self) -> None:
        """
        This method zooms out the field.

        :return:
        """
        if self.__square_size <= self.__min_square_size:
            return
        self.__square_size //= self.__scale_coefficient
        self.__scale_level *= self.__scale_coefficient
        self.__canvas.scale('all', self.__padding, self.__padding,
                            1 / self.__scale_coefficient,
                            1 / self.__scale_coefficient)

    def __move_right(self) -> None:
        """
        This method moves right the view of the field.

        :return:
        """
        if self.__left_shift + self.__scale_level > self.__width:
            delta = -(self.__width - self.__left_shift) * self.__square_size
            self.__left_shift = self.__width
        else:
            delta = -self.__scale_level * self.__square_size
            self.__left_shift += self.__scale_level
        self.__canvas.move('all', delta, 0)

    def __move_left(self) -> None:
        """
        This method moves left the view of the field.

        :return:
        """
        if self.__left_shift - self.__scale_level < 0:
            delta = self.__left_shift * self.__square_size
            self.__left_shift = 0
        else:
            delta = self.__scale_level * self.__square_size
            self.__left_shift -= self.__scale_level
        self.__canvas.move('all', delta, 0)

    def __move_down(self) -> None:
        """
        This method moves down the view of the field.

        :return:
        """
        if self.__up_shift + self.__scale_level > self.__height:
            delta = -(self.__height - self.__up_shift) * self.__square_size
            self.__up_shift = self.__height
        else:
            delta = -self.__scale_level * self.__square_size
            self.__up_shift += self.__scale_level
        self.__canvas.move('all', 0, delta)

    def __move_up(self) -> None:
        """
        This method moves up the view of the field.

        :return:
        """
        if self.__up_shift - self.__scale_level < 0:
            delta = self.__up_shift * self.__square_size
            self.__up_shift = 0
        else:
            delta = self.__scale_level * self.__square_size
            self.__up_shift -= self.__scale_level
        self.__canvas.move('all', 0, delta)

    def __process_key_release(self, event: Event) -> None:
        """
        This method processes a key release event, it should be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        key = event.keysym
        if key == 'Alt_L' or key == 'Alt_R':
            self.__alt_pressed = False
        elif key == 'Shift_L' or key == 'Shift_R':
            self.__shift_pressed = False

    def __change_square(self, event: Event) -> None:
        """
        This method changes a square on mouse click, it should be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        row_index = (event.y - self.__padding) // \
            self.__square_size + self.__up_shift
        col_index = (event.x - self.__padding) // \
            self.__square_size + self.__left_shift
        if row_index < 0 or row_index >= self.__height:
            return
        if col_index < 0 or col_index >= self.__width:
            return
        if self.__alt_pressed:
            self.__change_special_square(row_index, col_index,
                                         SquareType.START)
        elif self.__shift_pressed:
            self.__change_special_square(row_index, col_index,
                                         SquareType.FINISH)
        else:
            self.__change_normal_square(row_index, col_index)

    def __change_normal_square(self, row_index: int, col_index: int) -> None:
        """
        This method changes a square from free to blocked and vice versa.

        :param row_index: row index.
        :param col_index: column index.
        :return:
        """
        square = self.__field_data[row_index][col_index]
        if square.square_type == SquareType.BLOCKED:
            square.change_type(SquareType.FREE)
        elif square.square_type == SquareType.FREE:
            square.change_type(SquareType.BLOCKED)

    def __change_special_square(self, row_index: int, col_index: int,
                                square_type: SquareType) -> None:
        """
        This method changes the position of the start or the finish.

        :param row_index: new row index.
        :param col_index: new column index.
        :param square_type: start or finish.
        :return:
        """
        if self.__field_data[row_index][col_index].square_type == square_type:
            return
        if square_type == SquareType.START:
            old_row = self.__start_position[0]
            old_col = self.__start_position[1]
            self.__start_position = (row_index, col_index)
        elif square_type == SquareType.FINISH:
            old_row = self.__finish_position[0]
            old_col = self.__finish_position[1]
            self.__finish_position = (row_index, col_index)
        else:
            return
        start_row, start_col = self.__start_position
        finish_row, finish_col = self.__finish_position
        self.__field_data[old_row][old_col]. \
            change_type(SquareType.FREE)
        self.__field_data[start_row][start_col]. \
            change_type(SquareType.START)
        self.__field_data[finish_row][finish_col]. \
            change_type(SquareType.FINISH)

    def __draw_square(self, row_index: int, col_index: int) -> None:
        """
        This method draws a square at given coordinates.

        :param row_index: row index.
        :param col_index: column index.
        :return:
        """
        x0 = self.__padding + \
            (col_index - self.__left_shift) * self.__square_size
        y0 = self.__padding + \
            (row_index - self.__up_shift) * self.__square_size
        self.__field_data[row_index][col_index] \
            .draw(self.__square_size, (x0, y0))

    def __get_width_in_squares(self) -> int:
        """
        This method returns the number of squares that would be enough to cover the frame horizontally.

        :return: the number of squares.
        """
        return self.get_frame_width() // self.__square_size + 1

    def __get_height_in_squares(self) -> int:
        """
        This method returns the number of squares that would be enough to cover the frame vertically.

        :return: the number of squares.
        """
        return self.get_frame_height() // self.__square_size + 1
