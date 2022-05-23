from csv import reader, writer
from itertools import product
from json import dump, load
from os.path import exists
from random import random, randrange
from tkinter import BOTH, Canvas, Event, Frame, Misc, TOP

from map_editor.square import Square, SquareType


class Field(Frame):
    """
    This class provides methods for generating a field and drawing it on the
    screen.

    :param master: the master tkinter widget.
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
    __left_shift = 0
    __up_shift = 0
    __start_position = (0, 0)
    __start_square = None
    __finish_position = (0, 0)
    __finish_square = None
    __area_start = (0, 0)
    __area = None
    __alt_pressed = False
    __shift_pressed = False
    __current_type = SquareType.PLAIN
    __editor_mode = True

    def __init__(self, master: Misc, width: int = 10, height: int = 10,
                 density: float = 0.5) -> None:
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__density = density
        self.__field_data = []
        self.__canvas = Canvas(self)
        self.__configure()

    def generate_random(self) -> None:
        """
        This method randomly fills the field.

        :return:
        """
        self.reset()
        start_row = randrange(self.__height)
        start_col = randrange(self.__width)
        finish_row = randrange(self.__height)
        finish_col = randrange(self.__width)
        for row, col in product(range(self.__height), range(self.__width)):
            if row == start_row and col == start_col or \
                    row == finish_row and col == finish_col:
                continue
            if random() < self.__density:
                self.__field_data[row][col].change_type(SquareType.MOUNTAIN)

    def save_json(self, file_name: str) -> None:
        """
        This method saves the field to a json file.

        :param file_name: output file name.
        :return:
        """
        field_data = {
            'width': self.__width,
            'height': self.__height,
            'field': [[self.__field_data[row][col].square_type
                       for col in range(self.__width)]
                      for row in range(self.__height)],
            'start': self.__start_position,
            'finish': self.__finish_position,
        }
        with open(file_name, 'w') as file:
            dump(field_data, file, indent=2)

    def load_json(self, file_name: str) -> None:
        """
        This method loads the field from a json file.

        :param file_name: input file name.
        :return:
        """
        if not self.__check_file(file_name):
            return
        with open(file_name, 'r') as file:
            field_data = load(file)
        self.reset(field_data['width'], field_data['height'])
        for row, col in product(range(self.__height), range(self.__width)):
            self.__field_data[row][col].change_type(
                field_data['field'][row][col])
        self.__start_position = field_data['start']
        self.__finish_position = field_data['finish']

    def save_csv(self, file_name: str) -> None:
        """
        This method saves the field to a csv file.

        :param file_name: output file name.
        :return:
        """
        field_data = [(self.__width, self.__height)]
        field_data += [[int(self.__field_data[row][col].square_type)
                        for col in range(self.__width)]
                       for row in range(self.__height)]
        field_data.append(self.__start_position)
        field_data.append(self.__finish_position)
        with open(file_name, 'w') as file:
            file_writer = writer(file)
            file_writer.writerows(field_data)

    def load_csv(self, file_name: str) -> None:
        """
        This method loads the field from a csv file.

        :param file_name: input file name.
        :return:
        """
        if not self.__check_file(file_name):
            return
        with open(file_name, 'r') as file:
            file_reader = reader(file)
            field_data = []
            for line in file_reader:
                field_data.append(list(map(int, line)))
        self.reset(*field_data[0])
        for row, col in product(range(self.__height), range(self.__width)):
            self.__field_data[row][col].change_type(field_data[row + 1][col])
        self.__start_position = field_data[-2]
        self.__finish_position = field_data[-1]

    def save_txt(self, file_name: str) -> None:
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

    def load_txt(self, file_name: str) -> None:
        """
        This method loads the field from a text file.

        :param file_name: input file name.
        :return:
        """
        if not self.__check_file(file_name):
            return
        with open(file_name, 'r') as file:
            new_width, new_height = map(int, file.readline().split())
            self.reset(new_width, new_height)
            for row in range(self.__height):
                square_types = list(map(lambda x: SquareType(int(x)),
                                        file.readline().split()))
                for col in range(self.__width):
                    self.__field_data[row][col].change_type(square_types[col])
            self.__start_position = tuple(map(int, file.readline().split()))
            self.__finish_position = tuple(map(int, file.readline().split()))

    def reset(self, new_width: int = None, new_height: int = None) -> None:
        """
        This method fills the field with free squares and sets start and finish at (0,0).

        :param new_width: the new width of the field.
        :param new_height: the new height of the field.
        :return:
        """
        self.__canvas.delete('all')
        if new_width is not None:
            self.__width = new_width
        if new_height is not None:
            self.__height = new_height
        self.__field_data = [[Square(self.__canvas, size=self.__square_size)
                              for _ in range(self.__width)]
                             for _ in range(self.__height)]
        self.__start_position = (0, 0)
        self.__finish_position = (0, 0)
        self.__draw()

    def change_mode(self) -> None:
        """
        Changes mode to editor and back.

        :return:
        """
        self.__remove_binds()
        if self.__editor_mode:
            self.__editor_mode = False
            self.__add_other_binds()
            self.__start_square = \
                Square(self.__canvas, SquareType.START, self.__square_size,
                       self.__get_position_from_index(*self.__start_position))
            self.__start_square.draw()
            self.__finish_square = \
                Square(self.__canvas, SquareType.FINISH, self.__square_size,
                       self.__get_position_from_index(*self.__finish_position))
            self.__finish_square.draw()
        else:
            self.__editor_mode = True
            self.__add_editor_binds()
            self.__start_square.delete()
            self.__start_square = None
            self.__finish_square.delete()
            self.__finish_square = None

    def zoom_in(self) -> None:
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

    def zoom_out(self) -> None:
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

    def move_right(self) -> None:
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

    def move_left(self) -> None:
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

    def move_down(self) -> None:
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

    def move_up(self) -> None:
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

    def change_square_type(self, new_type: int) -> None:
        """
        This method changes the current square type.

        :param new_type: id of the new square type (0 to 9).
        :return:
        """
        if SquareType.has_value(new_type):
            self.__current_type = SquareType(new_type)

    def __configure(self) -> None:
        """
        This method does initial configuration for this widget.

        :return:
        """
        self.pack(fill=BOTH, side=TOP, expand=1)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__add_editor_binds()
        self.reset()

    def __draw(self) -> None:
        """
        This method draws the field.

        :return:
        """
        for row, col in product(range(self.__height), range(self.__width)):
            self.__draw_square(row, col)

    def __add_editor_binds(self) -> None:
        """
        This method adds binds to this class to process user input in the
        editor mode.

        :return:
        """
        self.__canvas.bind('<Button-1>', self.__change_square)
        self.__canvas.bind('<B1-Motion>', self.__change_square)
        self.__canvas.bind('<Button-2>', self.__set_area_start)
        self.__canvas.bind('<B2-Motion>', self.__select_area)
        self.__canvas.bind('<ButtonRelease-2>', self.__change_area)

    def __add_other_binds(self) -> None:
        """
        This method adds binds to this class to process user input when not in
        the editor mode.

        :return:
        """
        self.__canvas.bind('<Button-1>', self.__change_start)
        self.__canvas.bind('<B1-Motion>', self.__change_start)
        self.__canvas.bind('<Button-2>', self.__change_finish)
        self.__canvas.bind('<B2-Motion>', self.__change_finish)

    def __remove_binds(self) -> None:
        """
        This method removes oll binds that depend on the current mode.

        :return:
        """
        self.__canvas.unbind('<Button-1>')
        self.__canvas.unbind('<B1-Motion>')
        self.__canvas.unbind('<Button-2>')
        self.__canvas.unbind('<B2-Motion>')
        self.__canvas.unbind('<ButtonRelease-2>')

    @staticmethod
    def __check_file(file_name: str) -> bool:
        """
        This method checks if a file exists and prints a notification if it
        doesn't.

        :param file_name: name of the file to check.
        :return: true if the file exists.
        """
        if not exists(file_name):
            print(f'Could not load "{file_name}", file does not exist.')
            return False
        return True

    def __change_square(self, event: Event) -> None:
        """
        This method changes a square, it should be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        row, col = self.__get_index_from_position(event.x, event.y)
        if row < 0 or row >= self.__height:
            return
        if col < 0 or col >= self.__width:
            return
        self.__field_data[row][col].change_type(self.__current_type)

    def __change_start(self, event: Event) -> None:
        """
        This method changes the position of the start square, it should be used
        in widget.bind.

        :param event: tkinter event.
        :return:
        """
        self.__start_position = self.__limit_indices(
            *self.__get_index_from_position(event.x, event.y))
        position = self.__get_position_from_index(*self.__start_position)
        self.__start_square.draw(self.__square_size, position)

    def __change_finish(self, event: Event) -> None:
        """
        This method changes the position of the finish square, it should be
        used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        self.__finish_position = self.__limit_indices(
            *self.__get_index_from_position(event.x, event.y))
        position = self.__get_position_from_index(*self.__finish_position)
        self.__finish_square.draw(self.__square_size, position)

    def __set_area_start(self, event: Event) -> None:
        """
        This method sets the start of an area that will be changed, it should
        be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        self.__area_start = event.x, event.y

    def __select_area(self, event: Event) -> None:
        """
        This method selects an area that will be changed and draws a rectangle
        around it, it should be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        start_x, start_y = self.__area_start
        if self.__area is None:
            self.__area = self.__canvas.create_rectangle(start_x, start_y,
                                                         event.x, event.y,
                                                         fill='',
                                                         outline='blue')
        else:
            self.__canvas.coords(self.__area, start_x, start_y,
                                 event.x, event.y)

    def __change_area(self, event: Event) -> None:
        """
        This method changes an area of squares, it should be used in
        widget.bind.

        :param event: tkinter event.
        :return:
        """
        finish_row, finish_col = \
            self.__get_index_from_position(event.x, event.y)
        start_row, start_col = \
            self.__get_index_from_position(*self.__area_start)
        if start_row > finish_row:
            start_row, finish_row = finish_row, start_row
        if start_col > finish_col:
            start_col, finish_col = finish_col, start_col
        if start_row >= self.__height or finish_row < 0 or \
                start_col >= self.__width or finish_col < 0:
            self.__canvas.delete(self.__area)
            self.__area = None
            return
        finish_row, finish_col = self.__limit_indices(finish_row, finish_col)
        start_row, start_col = self.__limit_indices(start_row, start_col)
        for row, col in product(range(start_row, finish_row + 1),
                                range(start_col, finish_col + 1)):
            self.__field_data[row][col].change_type(self.__current_type)
        self.__canvas.delete(self.__area)
        self.__area = None

    def __draw_square(self, row_index: int, col_index: int) -> None:
        """
        This method draws a square at given coordinates.

        :param row_index: row index.
        :param col_index: column index.
        :return:
        """
        self.__field_data[row_index][col_index] \
            .draw(self.__square_size,
                  self.__get_position_from_index(row_index, col_index))

    def __get_position_from_index(self, row_index: int, col_index: int) -> tuple:
        """
        This method returns coordinates of the top left point of the square
        given its row and column indices.

        :param row_index: index of the row of the square.
        :param col_index: index of the column of the square.
        :return: coordinates of the top left point of the square.
        """
        x = self.__padding + \
            (col_index - self.__left_shift) * self.__square_size
        y = self.__padding + \
            (row_index - self.__up_shift) * self.__square_size
        return x, y

    def __get_index_from_position(self, x: int, y: int) -> tuple:
        """
        This method returns a row and a column of a square given coordinates of
        its inside point.

        :param x: x coordinate of the square.
        :param y: y coordinate of the square.
        :return: indices of the row and the column of the square.
        """
        row_index = (y - self.__padding) // \
            self.__square_size + self.__up_shift
        col_index = (x - self.__padding) // \
            self.__square_size + self.__left_shift
        return row_index, col_index

    def __limit_indices(self, row_index: int, col_index: int) -> tuple:
        """
        This method makes given indices fit inside the field.

        :param row_index: index of the row.
        :param col_index: index of the column.
        :return: limited indices.
        """
        if row_index >= self.__height:
            row_index = self.__height - 1
        if row_index < 0:
            row_index = 0
        if col_index >= self.__width:
            col_index = self.__width - 1
        if col_index < 0:
            col_index = 0
        return row_index, col_index