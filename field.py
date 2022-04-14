from csv import reader, writer
from enum import IntEnum
from itertools import product
from json import dump, load
from os.path import exists
from random import random, randrange
from tkinter import BOTH, Canvas, Event, Frame, TOP


class SquareType(IntEnum):
    FREE = 1
    BLOCKED = 2
    TYPE2 = 3
    TYPE3 = 4
    TYPE4 = 5
    TYPE5 = 6
    START = 10
    FINISH = 11

    @classmethod
    def has_value(cls, value: int) -> bool:
        """
        This method checks if this class contains a certain value.

        :param value: the value for which to check if this class contains it.
        :return: true if this class contains the value.
        """
        return value in cls._value2member_map_


SquareTypeColor = {
    SquareType.FREE: '#009000',
    SquareType.BLOCKED: '#900000',
    SquareType.TYPE2: '#a06000',
    SquareType.TYPE3: '#00b090',
    SquareType.TYPE4: '#900090',
    SquareType.TYPE5: '#666666',
    SquareType.START: '#000090',
    SquareType.FINISH: '#c0a000'
}


class Square:
    """
    This class contains information about one square on the canvas and provides
    methods to change its parameters.

    :param canvas: the canvas on which to draw the square.
    :param square_type: the type of the square.
    :param size: the size of the square.
    :param position: the position of the top left corner of the square.
    :param square_id: the id of the square on the canvas.
    """

    def __init__(self, canvas: Canvas,
                 square_type: SquareType = SquareType.FREE,
                 size: int = 0, position: tuple = (0, 0),
                 square_id: int = None) -> None:
        self.__canvas = canvas
        self.square_type = square_type
        self.position = position
        self.size = size
        self.__square_id = square_id

    def draw(self, size: int = None, position: tuple = None) -> None:
        """
        This method changes the size and the position of this square and draws
        it on the canvas.

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
            color = SquareTypeColor[self.square_type]
            self.__canvas.itemconfig(self.__square_id,
                                     fill=color, outline=color)

    def get_coordinates(self) -> tuple:
        """
        This method returns the position of the top left and bottom right
        corners of this square.

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
        color = SquareTypeColor[self.square_type]
        self.__square_id = self.__canvas.create_rectangle(
            x0, y0, x1, y1, fill=color, outline=color)


class Field(Frame):
    """
    This class provides methods for generating a field and drawing it on the
    screen.

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
    __finish_position = (0, 0)
    __area_start = (0, 0)
    __area = None
    __alt_pressed = False
    __shift_pressed = False
    __current_type = SquareType.FREE

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
        start_row = randrange(self.__height)
        start_col = randrange(self.__width)
        self.__change_special_square(start_row, start_col, SquareType.START)
        finish_row = randrange(self.__height)
        finish_col = randrange(self.__width)
        self.__change_special_square(finish_row, finish_col, SquareType.FINISH)
        for row, col in product(range(self.__height), range(self.__width)):
            if row == start_row and col == start_col or \
                    row == finish_row and col == finish_col:
                continue
            if random() < self.__density:
                self.__field_data[row][col].change_type(SquareType.BLOCKED)

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
        for row, col in product(range(self.__height), range(self.__width)):
            self.__draw_square(row, col)

    def __add_binds(self) -> None:
        """
        This method adds binds to this class to process user input.

        :return:
        """
        self.__canvas.bind('<Button-1>', self.__change_square)
        self.__canvas.bind('<B1-Motion>', self.__change_square)
        self.__canvas.bind('<Button-2>', self.__set_area_start)
        self.__canvas.bind('<B2-Motion>', self.__select_area)
        self.__canvas.bind('<ButtonRelease-2>', self.__change_area)
        self.focus_set()
        self.bind('<KeyPress>', self.__process_key_press)
        self.bind('<KeyRelease>', self.__process_key_release)

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

    def __process_key_press(self, event: Event) -> None:
        """
        This method processes a key press event, it should be used in
        widget.bind.

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
        elif str.isdigit(key) and SquareType.has_value(int(key)):
            self.__current_type = SquareType(int(key))

    def __process_key_release(self, event: Event) -> None:
        """
        This method processes a key release event, it should be used in
        widget.bind.

        :param event: tkinter event.
        :return:
        """
        key = event.keysym
        if key == 'Alt_L' or key == 'Alt_R':
            self.__alt_pressed = False
        elif key == 'Shift_L' or key == 'Shift_R':
            self.__shift_pressed = False

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

    def __change_square(self, event: Event) -> None:
        """
        This method changes a square, it should be used in widget.bind.

        :param event: tkinter event.
        :return:
        """
        row, col = self.__get_index_from_coordinates(event.x, event.y)
        if row < 0 or row >= self.__height:
            return
        if col < 0 or col >= self.__width:
            return
        if self.__alt_pressed:
            self.__change_special_square(row, col, SquareType.START)
        elif self.__shift_pressed:
            self.__change_special_square(row, col, SquareType.FINISH)
        else:
            self.__change_normal_square(row, col)

    def __change_normal_square(self, row_index: int, col_index: int) -> None:
        """
        This method changes a square to the current chosen type if it is not
        the start or the finish.

        :param row_index: row index.
        :param col_index: column index.
        :return:
        """
        square = self.__field_data[row_index][col_index]
        if square.square_type == SquareType.START or \
                square.square_type == SquareType.FINISH:
            return
        square.change_type(self.__current_type)

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
            self.__get_index_from_coordinates(event.x, event.y)
        start_row, start_col = \
            self.__get_index_from_coordinates(*self.__area_start)
        if start_row > finish_row:
            start_row, finish_row = finish_row, start_row
        if start_col > finish_col:
            start_col, finish_col = finish_col, start_col
        finish_row = min(self.__height, finish_row)
        finish_col = min(self.__width, finish_col)
        for row, col in product(range(start_row, finish_row + 1),
                                range(start_col, finish_col + 1)):
            self.__change_normal_square(row, col)
        self.__canvas.delete(self.__area)
        self.__area = None

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
        This method returns the number of squares that would be enough to cover
        the frame horizontally.

        :return: the number of squares.
        """
        return self.get_frame_width() // self.__square_size + 1

    def __get_height_in_squares(self) -> int:
        """
        This method returns the number of squares that would be enough to cover
        the frame vertically.

        :return: the number of squares.
        """
        return self.get_frame_height() // self.__square_size + 1

    def __get_index_from_coordinates(self, x: int, y: int) -> tuple:
        """
        This method returns a row and a column of a square given coordinates of
        its inside point.

        :param x: x coordinate of the square.
        :param y: y coordinate of the square.
        :return: indices of the row and the column.
        """
        row_index = (y - self.__padding) // \
            self.__square_size + self.__up_shift
        col_index = (x - self.__padding) // \
            self.__square_size + self.__left_shift
        return min(row_index, self.__height - 1), \
            min(col_index, self.__width - 1)
