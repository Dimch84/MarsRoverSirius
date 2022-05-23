from requests import delete, get, post
from json import dumps, load, loads

from tkinter import *
from tkinter.filedialog import askopenfilename, askopenfilenames
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring

from application.map import Map
from application.map_drawing import draw

from constants import url

from map_editor.editor import Editor


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
                y = 250,
                height = 90,
                width = 300,
                bordermode='outside')


        self.button_make_map = Button(self.master,
                   text ="MAKE MAP",
                   command = self.make_map,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        self.button_make_map.place(x = 350,
                y = 150,
                height = 90,
                width = 300,
                bordermode='outside')


        self.button_register = Button(self.master,
                    text ="REGISTER",
                    command = self.register,
                    bg = 'thistle2',
                    activebackground = 'thistle1')

        self.button_register.place(x = 350,
                y = 350,
                height = 90,
                width = 300,
                bordermode='outside')


        self.button_delete = Button(self.master,
                    text="DELETE",
                    command=self.delete,
                    bg='thistle2',
                    activebackground='thistle1')

        self.button_delete.place(x=350,
                y=450,
                height=90,
                width=300,
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

        files_name = askopenfilenames(title = 'Choose a file(s)')

        direction_paths = []
        teams = loads(get(url).content)
        for team in teams:
            try:
                answer = loads(post(team['url'], json=dumps(field_data)).content)
                direction_paths.append(answer[1])
            except EXCEPTION:
                print('Connection error')

        draw(self.master, Map(len(field), len(field[0]),
             field, start, goal, direction_paths, radius), files_name)

    @staticmethod
    def register():
        team_name = askstring('Team name',
                              'Enter your team\'s name:')
        if not team_name:
            return
        team_url = askstring('Service url',
                             'Enter your service\'s url:')
        if not team_url:
            return
        post(url, json=dumps({'name': team_name, 'url': team_url}))

    @staticmethod
    def delete():
        team_name = askstring('Team name',
                              'Enter your team\'s name:')
        if not team_name:
            return
        delete(url + team_name)
