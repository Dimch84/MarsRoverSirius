from tkinter import Misc, Toplevel

from map_editor.field import Field
from map_editor.ui import UI


class Editor:
    def __init__(self, master: Misc):
        self.__slave = Toplevel(master)
        self.__configure()

    def __configure(self):
        self.__slave.title("Map editor")
        self.__slave.geometry("{0}x{1}+0+0".format(
            self.__slave.winfo_screenwidth(),
            self.__slave.winfo_screenheight()))
        field = Field(self.__slave)
        UI(self.__slave, field)
