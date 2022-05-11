import json
import tkinter
from tkinter import *
from inspect import getmro
from json import dump, dumps, load, loads
from pathlib import PurePath
from requests import get, post

from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring

from application.map import Map
from application.map_drawing import draw

from map_editor.editor import Editor


class Application:
    url = 'http://127.0.0.1:5000/maps'  # TODO: better organize urls

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
                y = 450,
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

        self.button_upload_map = Button(self.master,
                   text ="UPLOAD MAP",
                   command = self.upload_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_upload_map.place(x = 350,
                y = 550,
                height = 90,
                width = 300,
                bordermode='outside')

        self.button_download_map = Button(self.master,
                   text ="DOWNLOAD MAP",
                   command = self.download_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_download_map.place(x = 350,
                y = 650,
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
        def get_direction_path(path: [(int, int)]) -> [(int, int)]:
            direction_path = []
            for i in range(len(path[:-1])):
                current_cell, next_cell = path[i], path[i + 1]
                direction_path.append((next_cell[0] - current_cell[0], next_cell[1] - current_cell[1]))
            return direction_path

        self.master.withdraw()
        file_name = askopenfilename()

        with open(file_name, 'r') as file:
            field_data = load(file)
        start = field_data['start']
        finish = field_data['finish']
        field = field_data['field']

        form = dumps({'start': start, 'finish': finish, 'field': field, 'name': PurePath(file_name).name})
        post(self.url, json=form)

        path_length, path = loads(get(self.url + '/test2.json').content)

        direction_path = get_direction_path(path) # путь из дельт


        draw(self.master, Map(len(field), len(field[0]),
            field, start, finish, direction_path, -1))

    def upload_map(self):
        file_name = askopenfilename()
        with open(file_name, 'r') as file:
            field_data = load(file)
        start = field_data['start']
        finish = field_data['finish']
        field = field_data['field']

        form = dumps({'start': start, 'finish': finish, 'field': field, 'name': PurePath(file_name).name})
        post(self.url, json=form)

    def download_map(self):
        all_maps = loads(get(self.url).content)
        names = list(all_maps)
        print(all_maps)
        name = askstring('Choose map', 'map_name.json')
        if name not in names:
            return
        file_name = asksaveasfilename()
        with open(file_name, 'w') as file:
            dump(all_maps[name], file)
