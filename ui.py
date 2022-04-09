from tkinter import BOTH, BOTTOM, Button, Canvas, Frame, LEFT

from field import Field


class UI(Frame):
    __button_height = 10

    def __init__(self, field: Field):
        super().__init__()
        self.__field = field
        # self.__canvas = Canvas(self)
        self.pack(fill=BOTH, side=BOTTOM, expand=0)
        # self.__canvas.pack(fill=BOTH, expand=1)
        self.__save_button = Button()
        self.__load_button = Button()
        self.__random_button = Button()
        self.__configure()

    def __configure(self):
        self.__configure_save_button()
        self.__configure_load_button()
        self.__configure_random_button()

    def __configure_save_button(self):
        self.__configure_button(self.__save_button)
        self.__save_button.config(text='Save',
                                  command=self.__save)

    def __configure_load_button(self):
        self.__configure_button(self.__load_button)
        self.__load_button.config(text='Load',
                                  command=self.__load)

    def __configure_random_button(self):
        self.__configure_button(self.__random_button)
        self.__random_button.config(text='Generate random',
                                    command=self.__generate_random)

    def __configure_button(self, button: Button):
        button.pack(fill=BOTH, side=LEFT, expand=1)
        button.config(height=self.__button_height)

    def __save(self):  # TODO finish
        self.__field.save_json('output2.json')
        print('Saved!')

    def __load(self):  # TODO finish
        self.__field.load_json('input2.json')
        print('Loaded!')

    def __generate_random(self):  # TODO finish
        self.__field.generate_random()
        print('Randomised!')
