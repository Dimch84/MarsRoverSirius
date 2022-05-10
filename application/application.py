import json
import tkinter
from tkinter import *
from inspect import getmro
from json import load, loads
from requests import get, post

from tkinter.filedialog import askopenfilename

from application.map import Map
from application.map_drawing import draw

from map_editor.editor import Editor


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
                y = 550, 
                height = 90, 
                width = 300, 
                bordermode='outside')


        self.button = Button(self.master, 
                   text ="MAP", 
                   command = self.draw_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button.place(x = 350,
                y = 450, 
                height = 90, 
                width = 300, 
                bordermode='outside')


        self.button_make_map = Button(self.master, 
                   text ="MAKE MAP", 
                   command = self.make_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_make_map.place(x = 350,
                y = 350, 
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

        def f(array: [[int]]):
            string_array = []
            for subarray in array:
                string_array.append(''.join(map(str,subarray)))
            return string_array

        self.master.withdraw()
        file_name = askopenfilename()

        with open(file_name, 'r') as file:
            field_data = load(file)
        start = field_data['start']
        goal = field_data['finish']
        field = field_data['field']

        url = 'http://127.0.0.1:5000'  # TODO: better organize urls
        form = json.dumps({'start': start, 'goal': goal, 'field': f(field)})
        path_length, path = loads(post(url, json=form).content)

        # path_length, path = A_star.call(start, goal, f(field))
        direction_path = get_direction_path(path) # путь из дельт
        
        
        draw(self.master, Map(len(field), len(field[0]), 
            field, start, goal, direction_path, -1))
