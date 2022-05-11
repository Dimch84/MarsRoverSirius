from tkinter import Misc

from json import loads
from requests import get
from tkinter import END, Listbox, Toplevel
from constants import url


def load_fields_list(master: Misc) -> (Toplevel, Listbox, dict):
    """
    This method loads a fields list from service.

    :param master: master tkinter widget.
    :return: slave widget, listbox with all the fields,
             dictionary with all the fields.
    """
    slave = Toplevel(master)
    slave.title("All maps")

    fields_list = Listbox(slave)

    all_fields = loads(get(url).content)
    print(all_fields)
    for name in all_fields:
        description = all_fields[name]['description']
        fields_list.insert(END, f'{name}: {description}')

    fields_list.pack()
    return slave, fields_list, all_fields


def choose_field(fields_list: Listbox, all_fields: dict, fun, *args) -> None:
    """
    This method passes the chosen field to the method fun.

    :param fields_list: listbox with all the fields.
    :param all_fields: dictionary with all the fields.
    :param fun: method that will be called in the end.
    :param args: other arguments that will be passed to fun.
    :return:
    """
    selection = fields_list.curselection()
    if len(selection) == 0:
        return
    field_index = selection[-1]
    field_name = list(all_fields)[field_index]
    fun(all_fields[field_name], *args)


def f(array: [[int]]):
    string_array = []
    for subarray in array:
        string_array.append(''.join(map(str, subarray)))
    return string_array
