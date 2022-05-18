import tkinter
from tkinter import *
from inspect import getmro
from json import load
import os

from tkinter.filedialog import askopenfilename, askopenfilenames
from tkinter.messagebox import askyesno
from turtle import width

from application.map import Map
from application.map_drawing import draw

from map_editor.editor import Editor

from application.color_application import color


FILE_OUT = 'output.json'

class Application:
 
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x1000")
        self.master.title('Menu')
        self.master.bind_all('<Destroy>', self.on_destroy)

        self.button_exit = Button(self.master, 
                   text ="EXIT", 
                   command = self.exit,
                   bg = color.button_background,
                   activebackground = color.button_a_background)

        self.button_exit.place(x = 350,
                y = 550, 
                height = 90, 
                width = 300, 
                bordermode='outside')


        self.button = Button(self.master, 
                   text ="MAP", 
                   command = self.draw_map,
                   bg = color.button_background,
                   activebackground = color.button_a_background)

        self.button.place(x = 350,
                y = 450, 
                height = 90, 
                width = 300, 
                bordermode='outside')


        self.button_make_map = Button(self.master, 
                   text ="MAKE MAP", 
                   command = self.make_map,
                   bg = color.button_background,
                   activebackground = color.button_a_background)

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
        confirmed = askyesno('Exit',
                             'Are you sure you want to exit?')
        if not confirmed:
            return

        exit()
        #self.master.quit()

    def make_map(self):
        self.master.withdraw()
        Editor(self.master)

    def draw_map (self):

        def f(array: [[int]]):
            string_array = []
            for subarray in array:
                string_array.append(''.join(map(str,subarray)))
            return string_array


        # self.master.withdraw()
        file_name = askopenfilename(title = 'Choose a file map')

        with open(file_name, 'r') as file:
            field_data = load(file)
        width = field_data['width']
        height = field_data['height']
        start = field_data['start']
        goal = field_data['finish']
        field = field_data['field']
        radius = -1

        argv =  str(height) + ' ' + str(width) + ' '
        argv += str(start[0]) + ' ' + str(start[1]) + ' '
        argv += str(goal[0]) + ' ' + str(goal[1]) + ' '
        argv += str(radius) + ' '


        for i in range(height):
            for j in range(width):
                argv += str(field[i][j]) + ' ' 


        files_name = askopenfilenames(title = 'Choose a file(s)')

        direction_paths = []

        for file_name in files_name:

            os.system('touch ' + FILE_OUT)
            os.system('python3 ' + file_name + ' ' + FILE_OUT + ' ' + argv)

            with open(FILE_OUT, 'r') as file:
                field_data = load(file)
            direction_paths.append(field_data['path'])

            os.system('rm ' + FILE_OUT)

        draw(self.master, Map(len(field), len(field[0]), 
             field, start, goal, direction_paths, radius), files_name)
		

root = Tk()
Application (root)


