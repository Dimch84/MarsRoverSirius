import os, sys
from tkinter import *
from json import load

from tkinter.filedialog import askopenfilename

from map import Map
from map_drawing import draw

sys.path.insert(1, os.path.join(sys.path[0], '../src')) 
from a_star import A_star


sys.path.insert(1, os.path.join(sys.path[0], '../map_editor'))
from editor import Editor



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

    def on_destroy(self, event):
        self.master.deiconify()

    def exit(self):
        self.master.quit()

    def make_map(self):
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

        
        path_length, path = A_star.call(start, goal, f(field))
        direction_path = get_direction_path(path) # путь из дельт
        
        
        draw(self.master, Map(len(field), len(field[0]), 
            field, start, goal, direction_path, -1))
		

root = Tk()
Application (root)


