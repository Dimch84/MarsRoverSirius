from tkinter import *

from tkinter.filedialog import askopenfilename

from map import Map
from map_drawing import draw
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

        self.master.withdraw()
        file_name = askopenfilename()
        
        # TODO
        
        # launch example
        # draw(self.master, Map(4, 7, 
        #     [[1,0,1,1,1,1,0], [1,0,0,0,0,0,0], [1,0,1,1,1,0,0], [0,0,1,0,0,0,0]], 
        #     (3, 0), (3, 3), 'RUURRRRDDLL', -1))
		

root = Tk()
Application (root)


