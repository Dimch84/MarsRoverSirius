from tkinter import Tk, Canvas, Frame, BOTH

from map import Map

class Draw(Frame):
 
    def __init__(self, map : Map):
        super().__init__()
        self.initUI(map)
 
    def initUI(self, map : Map):
        self.master.title("Рисуем формы")
        self.pack(fill=BOTH, expand=1)
 
        canvas = Canvas(self)

        # #draw lines
        # for i in range (map.n):
        #     canvas.create_line (0, map.size_cell * i,
        #                        map.width, map.size_cell * i)

        # for i in range (map.m):
        #     canvas.create_line (map.size_cell * i, 0,
        #                        map.size_cell * i, map.height)

        # draw cell
        for i in range (map.m):
            for j in range (map.n):

                color_cell = 'lavender'
                if map.map[j][i] == 1:
                    color_cell = 'gray'

                canvas.create_rectangle(
                        map.size_cell * i, map.size_cell * j,
                        map.size_cell * (i + 1), map.size_cell * (j + 1),
                        outline = 'black', fill = color_cell, width = 1)

        canvas.pack(fill=BOTH, expand=1)
 
 

def map_drawing (map : Map) -> None:

    # init screen 
    root = Tk()
    ex = Draw(map)
    root.title("Map drawing")
    root.geometry("{0}x{1}+0+0".format(
                    map.width + 1, map.height + 1))


    root.mainloop()


map_drawing(Map(4, 7, 
            [[1,0,1,1,1,1,0], [1,0,0,0,0,0,0], [1,0,1,1,1,0,0], [0,0,1,0,0,0,0]], 
            (3, 0), (3, 3), 'RUURRRRDDLL'))