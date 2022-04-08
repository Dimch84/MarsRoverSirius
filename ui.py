from tkinter import BOTH, BOTTOM, Canvas, Frame


class UI(Frame):
    __field_width = 800
    __field_height = 800

    def __init__(self):
        super().__init__()
        self.__canvas = Canvas(self)
        self.pack(fill=BOTH, side=BOTTOM, expand=0)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__canvas.create_rectangle(self.__field_width, 0, 1000, self.__field_height, fill='white')
