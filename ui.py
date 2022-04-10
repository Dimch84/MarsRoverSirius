from tkinter import BOTH, BOTTOM, Button, Canvas, Frame, LEFT

from field import Field


class UI(Frame):
    """
    This class provides user interface.

    :param field: the field to which this ui should be attached.
    """
    __button_height = 10

    def __init__(self, field: Field):
        super().__init__()
        self.__field = field
        self.pack(fill=BOTH, side=BOTTOM, expand=0)
        self.__save_button = Button()
        self.__load_button = Button()
        self.__random_button = Button()
        self.__configure()

    def __configure(self):
        """
        This method configures all ui elements.

        :return:
        """
        self.__configure_save_button()
        self.__configure_load_button()
        self.__configure_random_button()

    def __configure_save_button(self):
        """
        This method configures the 'save' button.

        :return:
        """
        self.__configure_button(self.__save_button)
        self.__save_button.config(text='Save',
                                  command=self.__save)

    def __configure_load_button(self):
        """
        This method configures the 'load' button.

        :return:
        """
        self.__configure_button(self.__load_button)
        self.__load_button.config(text='Load',
                                  command=self.__load)

    def __configure_random_button(self):
        """
        This method configures the 'generate random' button.

        :return:
        """
        self.__configure_button(self.__random_button)
        self.__random_button.config(text='Generate random',
                                    command=self.__generate_random)

    def __configure_button(self, button: Button):
        """
        This method configures all buttons.

        :return:
        """
        button.pack(fill=BOTH, side=LEFT, expand=1)
        button.config(height=self.__button_height)

    def __save(self):  # TODO finish
        """
        This method saves the field to a file.

        :return:
        """
        self.__field.save_json('output2.json')
        print('Saved!')

    def __load(self):  # TODO finish
        """
        This method load a field from a file.

        :return:
        """
        self.__field.load_json('input2.json')
        print('Loaded!')

    def __generate_random(self):  # TODO finish
        """
        This method generates a random field.

        :return:
        """
        self.__field.generate_random()
        print('Randomised!')
