import json
import tkinter
from tkinter import *
from inspect import getmro
from json import dump, dumps, load, loads
from pathlib import PurePath
from requests import get, post, delete

from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno

from application.map import Map
from application.map_drawing import draw

from constants import url
from map_editor.editor import Editor
from utils import load_fields, choose_field


class Application:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x1000")
        self.master.title('Menu')
        self.master.bind_all('<Destroy>', self.on_destroy)

        self.button_exit = Button(self.master,
                   text ="EXIT",
                   command = self.exit,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_exit.place(x = 350,
                y = 650,
                height = 90,
                width = 300,
                bordermode='outside')


        self.button = Button(self.master,
                   text ="MAP",
                   command = self.draw_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button.place(x = 350,
                y = 350,
                height = 90,
                width = 300,
                bordermode='outside')


        self.button_make_map = Button(self.master,
                   text ="MAKE MAP",
                   command = self.make_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_make_map.place(x = 350,
                y = 250,
                height = 90,
                width = 300,
                bordermode='outside')

        # self.button_upload_map = Button(self.master,
        #            text ="UPLOAD MAP",
        #            command = self.upload_map,
        #            bg = 'thistle2',
        #            activebackground = 'thistle1')
        #
        # self.button_upload_map.place(x = 350,
        #         y = 450,
        #         height = 90,
        #         width = 300,
        #         bordermode='outside')

        # self.button_download_map = Button(self.master,
        #            text ="DOWNLOAD MAP",
        #            command = self.download_map,
        #            bg = 'thistle2',
        #            activebackground = 'thistle1')
        #
        # self.button_download_map.place(x = 350,
        #         y = 550,
        #         height = 90,
        #         width = 300,
        #         bordermode='outside')

        self.button_manage_maps = Button(self.master,
                   text ="MANAGE MAPS",
                   command = self.manage_maps,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_manage_maps.place(x = 350,
                y = 450,
                height = 90,
                width = 300,
                bordermode='outside')

        self.master.mainloop()

    def on_destroy(self, event: Event):
        if event.widget.winfo_parent() == '.':
            self.master.deiconify()

    def exit(self):
        exit()
        self.master.quit()

    def make_map(self):
        self.master.withdraw()
        Editor(self.master)

    def draw_map (self):


        self.master.withdraw()

        slave, fields_list, all_fields = load_fields(self.master)
        choose_button = Button(slave, text="Draw solution",
                               command=lambda:
                               choose_field(fields_list, all_fields,
                                            self.__draw_chosen, slave))
        choose_button.pack()

    def upload_map(self):
        file_name = askopenfilename()
        with open(file_name, 'r') as file:
            field_data = load(file)
        start = field_data['start']
        finish = field_data['finish']
        field = field_data['field']

        form = dumps({'start': start, 'finish': finish,
                      'field': field, 'name': PurePath(file_name).name})
        post(url, json=form)

    def download_map(self):
        all_maps = loads(get(url).content)
        names = list(all_maps)
        name = askstring('Choose map', 'map_name.json')
        if name not in names:
            return
        file_name = asksaveasfilename()
        with open(file_name, 'w') as file:
            dump(all_maps[name], file)

    def manage_maps(self):
        self.master.withdraw()
        slave, fields_list, all_fields = load_fields(self.master)
        delete_button = Button(slave, text="Delete",
                               command=lambda:
                               choose_field(fields_list, all_fields,
                                            self.__delete_chosen, fields_list))
        delete_button.pack()

    @staticmethod
    def __delete_chosen(field, fields_list: Listbox):
        confirmed = askyesno('Delete map',
                             'Are you sure you want '
                             'to delete the chosen map?')
        if not confirmed:
            return
        fields_list.delete(ANCHOR)
        field_name = field['name']
        delete(url + f'/{field_name}')

    def __draw_chosen(self, field, slave):
        def get_direction_path(path: [(int, int)]) -> [(int, int)]:
            direction_path = []
            for i in range(len(path[:-1])):
                current_cell, next_cell = path[i], path[i + 1]
                direction_path.append((next_cell[0] - current_cell[0], next_cell[1] - current_cell[1]))
            return direction_path

        slave.destroy()
        self.master.withdraw()
        field_name = field['name']
        path_length, path = loads(get(url + f'/{field_name}').content)
        direction_path = get_direction_path(path)
        draw(self.master, Map(len(field['field']), len(field['field'][0]),
             field['field'], field['start'],
             field['finish'], direction_path, -1))
