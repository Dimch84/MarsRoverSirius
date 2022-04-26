from tkinter import Event, Misc, Toplevel

from map_editor.field import Field
from map_editor.ui import UI


class Editor:
    """
    This class creates an editor widget.

    :param master: the master tkinter widget.
    """
    def __init__(self, master: Misc) -> None:
        self.__slave = Toplevel(master)
        self.__field = None
        self.__ui = None
        self.__configure()

    def __configure(self) -> None:
        """
        This method configures the editor.

        :return:
        """
        self.__slave.title("Map editor")
        self.__slave.geometry("{0}x{1}+0+0".format(
            self.__slave.winfo_screenwidth(),
            self.__slave.winfo_screenheight()))
        self.__field = Field(self.__slave)
        self.__ui = UI(self.__slave, self.__field)
        self.__add_binds()

    def __add_binds(self) -> None:
        """
        This method adds binds to this class to process user input.

        :return:
        """
        self.__slave.focus_set()
        self.__slave.bind('<KeyPress>', self.__process_key_press)
        self.__slave.bind('<KeyRelease>', self.__process_key_release)

    def __process_key_press(self, event: Event) -> None:
        """
        This method processes a key press event, it should be used in
        widget.bind.

        :param event: tkinter event.
        :return:
        """
        key = event.keysym
        if key == 'plus':
            self.__field.zoom_in()
        elif key == 'minus':
            self.__field.zoom_out()
        elif key == 'Right':
            self.__field.move_right()
        elif key == 'Left':
            self.__field.move_left()
        elif key == 'Down':
            self.__field.move_down()
        elif key == 'Up':
            self.__field.move_up()
        elif str.isdigit(key):
            self.__field.change_square_type(int(key))
            self.__ui.change_square_type(int(key))

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
