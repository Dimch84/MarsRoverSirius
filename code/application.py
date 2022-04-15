from tkinter import *

from map import Map
from map_drawing import map_drawing, Draw

class Application(Frame):
 
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.master.title("Mars Rover")
        self.pack(fill = 'both', expand = 1)

        button_exit = Button(self, 
                   text ="EXIT", 
                   command = exit,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        button_exit.place(x = 350,
                y = 550, 
                height = 90, 
                width = 300, 
                bordermode='outside')



        button = Button(self, 
                   text ="MAP", 
                   command = map_drawing,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        button.place(x = 350,
                y = 450, 
                height = 90, 
                width = 300, 
                bordermode='outside')


        button_make_map = Button(self, 
                   text ="MAKE MAP", 
                   command = exit,
                   bg = 'thistle2',
                   activebackground = 'thistle1')

        button_make_map.place(x = 350,
                y = 350, 
                height = 90, 
                width = 300, 
                bordermode='outside')

        # b = Button(self, 
        #            text ="EXIT", 
        #            command = exit,
        #            height = 5,
        #            width = 35)
        #b.pack()

        # canvas = Canvas(self)
        # canvas.pack(fill = 'both', expand = 1)


def exit():
   exit()


def application () -> None:

    root = Tk()
    root.geometry("1000x1000")
    ex = Application()

    root.mainloop()


