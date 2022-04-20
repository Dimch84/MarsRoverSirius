from tkinter import BOTH, BOTTOM, Button, Frame, \
    Label, LEFT, Misc, OptionMenu, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askinteger
from enum import Enum

from map_editor.field import Field


class FileTypes(Enum):
    JSON = 'JSON'
    CSV = 'CSV'
    TXT = 'TXT'

    @classmethod
    def values(cls) -> list:
        """
        This method returns all the values of this Enum.

        :return: list of the values.
        """
        return list(map(lambda option: option.value, cls))


class UI(Frame):
    """
    This class provides user interface.

    :param root: the main tkinter widget.
    :param field: the field to which this ui should be attached.
    """
    __button_height = 5

    def __init__(self, master: Misc, field: Field) -> None:
        super().__init__(master)
        self.__master = master
        self.__field = field
        self.pack(fill=BOTH, side=BOTTOM, expand=0)
        self.__save_button = Button(master)
        self.__load_button = Button(master)
        self.__random_button = Button(master)
        self.__change_mode_button = Button(master)
        self.__new_button = Button(master)
        self.__exit_button = Button(master)
        self.__file_format = StringVar()
        self.__configure()

    def __configure(self) -> None:
        """
        This method configures all ui elements.

        :return:
        """
        self.__configure_save_button()
        self.__configure_load_button()
        self.__configure_random_button()
        self.__configure_change_mode_button()
        self.__configure_new_button()
        self.__configure_exit_button()
        self.__configure_file_format_menu()

    def __configure_save_button(self) -> None:
        """
        This method configures the 'save' button.

        :return:
        """
        self.__configure_button(self.__save_button)
        self.__save_button.config(text='Save',
                                  command=self.__save)

    def __configure_load_button(self) -> None:
        """
        This method configures the 'load' button.

        :return:
        """
        self.__configure_button(self.__load_button)
        self.__load_button.config(text='Load',
                                  command=self.__load)

    def __configure_random_button(self) -> None:
        """
        This method configures the 'randomise' button.

        :return:
        """
        self.__configure_button(self.__random_button)
        self.__random_button.config(text='Randomise',
                                    command=self.__generate_random)

    def __configure_change_mode_button(self) -> None:
        """
        This method configures the 'change mode' button.

        :return:
        """
        self.__configure_button(self.__random_button)
        self.__random_button.config(text='Change mode',
                                    command=self.__field.change_mode)

    def __configure_new_button(self) -> None:
        """
        This method configures the 'new' button.

        :return:
        """
        self.__configure_button(self.__new_button)
        self.__new_button.config(text='New',
                                 command=self.__create_new)

    def __configure_exit_button(self) -> None:
        """
        This method configures the 'exit' button.

        :return:
        """
        self.__configure_button(self.__exit_button)
        self.__exit_button.config(text='Exit',
                                  command=self.__exit)

    def __configure_file_format_menu(self) -> None:
        """
        This method configures file format option menu.

        :return:
        """
        menu_frame = Frame(self)
        menu_frame.pack(fill=BOTH, side=BOTTOM, expand=1)
        menu_label = Label(menu_frame, text='File format:')
        menu_label.pack(side=LEFT)
        self.__file_format.set(FileTypes.JSON.value)
        file_format_menu = OptionMenu(menu_frame,
                                      self.__file_format,
                                      *FileTypes.values())
        file_format_menu.pack(side=LEFT)

    def __configure_button(self, button: Button) -> None:
        """
        This method configures all buttons.

        :return:
        """
        button.pack(fill=BOTH, side=LEFT, expand=1)
        button.config(height=self.__button_height)

    def __save(self) -> None:
        """
        This method saves the field to a file.

        :return:
        """
        file_name = asksaveasfilename()
        if file_name == '':
            return
        file_type = self.__file_format.get()
        if file_type == FileTypes.JSON.value:
            self.__field.save_json(file_name)
        elif file_type == FileTypes.CSV.value:
            self.__field.save_csv(file_name)
        elif file_type == FileTypes.TXT.value:
            self.__field.save_txt(file_name)

    def __load(self) -> None:
        """
        This method loads the field from a file.

        :return:
        """
        confirmed = askyesno('Load',
                             'Are you sure you want to load a new map '
                             '(current map will not be saved)?')
        if not confirmed:
            return
        file_name = askopenfilename()
        if file_name == '':
            return
        file_type = self.__file_format.get()
        if file_type == FileTypes.JSON.value:
            self.__field.load_json(file_name)
        elif file_type == FileTypes.CSV.value:
            self.__field.load_csv(file_name)
        elif file_type == FileTypes.TXT.value:
            self.__field.load_txt(file_name)

    def __generate_random(self) -> None:
        """
        This method generates a random field.

        :return:
        """
        confirmed = askyesno('Randomise',
                             'Are you sure you want to randomise this map '
                             '(current state of the map will not be saved)?')
        if not confirmed:
            return
        self.__field.generate_random()

    def __create_new(self) -> None:
        """
        This method creates a new field.

        :return:
        """
        confirmed = askyesno('New',
                             'Are you sure you want to create a new map '
                             '(current map will not be saved)?')
        if not confirmed:
            return
        size = askinteger('Map size',
                          'Enter the size of a new map',
                          initialvalue=100)
        if size is None:
            return
        self.__field.reset(size, size)

    def __exit(self) -> None:
        """
        This method exits the app.

        :return:
        """
        confirmed = askyesno('Exit',
                             'Are you sure you want to exit '
                             '(current map will not be saved)?')
        if not confirmed:
            return
        self.__master.destroy()
