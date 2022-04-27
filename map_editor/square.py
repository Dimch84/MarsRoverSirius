from enum import IntEnum
from tkinter import Canvas


class SquareType(IntEnum):
    PLAIN = 1
    MOUNTAIN = 2
    SAND = 3
    CRATER = 4
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


SquareTypeName = {
    SquareType.PLAIN: 'Plain',
    SquareType.MOUNTAIN: 'Mountain',
    SquareType.SAND: 'Sand',
    SquareType.CRATER: 'Crater',
    SquareType.START: 'Start',
    SquareType.FINISH: 'Finish'

}


SquareTypeColor = {
    SquareType.PLAIN: '#009000',
    SquareType.MOUNTAIN: '#900000',
    SquareType.SAND: '#a06000',
    SquareType.CRATER: '#00b090',
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
                 square_type: SquareType = SquareType.PLAIN,
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

    def delete(self) -> None:
        """
        This method deletes this square.

        :return:
        """
        if self.__square_id is not None:
            self.__canvas.delete(self.__square_id)
        self.square_type = SquareType.PLAIN
        self.size = 0
        self.position = (0, 0)
        self.__square_id = None

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
