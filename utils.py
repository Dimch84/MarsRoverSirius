from tkinter import Misc

from json import loads
from requests import get, post
from tkinter import *  # ANCHOR, Button, END, Label, Listbox, Misc, Toplevel
from tkinter.messagebox import askokcancel, askyesno, showinfo
from tkinter.simpledialog import askinteger, askstring

from constants import url


def load_fields(master: Misc) -> (Toplevel, Listbox, dict):
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


def choose_field(fields_list, all_fields, fun, *args) -> None:
    selection = fields_list.curselection()
    if len(selection) == 0:
        return
    field_index = selection[-1]
    field_name = list(all_fields)[field_index]
    fun(all_fields[field_name], *args)
