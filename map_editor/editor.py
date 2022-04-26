from tkinter import Misc, Toplevel

from field import Field
from ui import UI


class Editor:
    """
    This class creates an editor widget.

    :param master: the master tkinter widget.
    """
    def __init__(self, master: Misc) -> None:
        self.__slave = Toplevel(master)
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
        field = Field(self.__slave)
        UI(self.__slave, field)
