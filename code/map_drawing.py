from tkinter import Tk, Canvas, Frame
import time

from map import Map

class Draw(Frame):
 
    def __init__(self, map : Map):
        super().__init__()
        self.initUI(map)
 
    def initUI(self, map : Map):

        self.master.title("Map")
        self.pack(fill = 'both', expand = 1)

        canvas = Canvas(self)
        canvas.pack(fill = 'both', expand = 1)

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

        
        # drawing movement Mars rover
        mars_rover_coordinate_y = map.start_point[0]
        mars_rover_coordinate_x = map.start_point[1]
        for step in map.mars_rover_path:
            
            new_mars_rover_coordinate_y = mars_rover_coordinate_y
            new_mars_rover_coordinate_x = mars_rover_coordinate_x
            
            # next coordinate
            if step == 'U':
                new_mars_rover_coordinate_y -= 1
            if step == 'D':
                new_mars_rover_coordinate_y += 1
            if step == 'R':
                new_mars_rover_coordinate_x += 1
            if step == 'L':
                new_mars_rover_coordinate_x -= 1

            canvas.create_line(
                            mars_rover_coordinate_x * map.size_cell + map.size_cell // 2,
                            mars_rover_coordinate_y * map.size_cell + map.size_cell // 2,
                            new_mars_rover_coordinate_x * map.size_cell + map.size_cell // 2,
                            new_mars_rover_coordinate_y * map.size_cell + map.size_cell // 2,
                            arrow = 'last',
                            dash = (5, 2))


            mars_rover_coordinate_x = new_mars_rover_coordinate_x
            mars_rover_coordinate_y = new_mars_rover_coordinate_y


        #out start and finish
        canvas.create_text(map.size_cell * map.start_point[1] + map.size_cell // 2, 
                            map.size_cell * map.start_point[0] + map.size_cell // 2,
                            text = 'START',
                            justify = 'center')
        canvas.create_text(map.size_cell * map.finish_point[1] + map.size_cell // 2, 
                            map.size_cell * map.finish_point[0] + map.size_cell // 2,
                            text = 'FINISH',
                            justify = 'center')


        
        # animation
        
        mars_rover_coordinate_y = mars_rover_coordinate_x = 1

        rover = canvas.create_rectangle(map.start_point[1] * map.size_cell, 
                                        map.start_point[0] * map.size_cell,
                                        (map.start_point[1] + 1) * map.size_cell,
                                        (map.start_point[0] + 1) * map.size_cell,
                                        outline = 'black', 
                                        fill = 'black', 
                                        width = 1)

        

        for step in map.mars_rover_path:
            # next coordinate
            if step == 'U':
                mars_rover_coordinate_y = -1
                mars_rover_coordinate_x = 0
            if step == 'D':
                mars_rover_coordinate_y = 1
                mars_rover_coordinate_x = 0
            if step == 'R':
                mars_rover_coordinate_y = 0
                mars_rover_coordinate_x = 1
            if step == 'L':
                mars_rover_coordinate_y = 0
                mars_rover_coordinate_x = -1

            #animation
            for i in range (map.size_cell):

                canvas.move(rover, 
                            mars_rover_coordinate_x, 
                            mars_rover_coordinate_y)
                self.update()
                canvas.after(10)
            

            


 

def map_drawing (map : Map) -> None:

    # init screen 
    root = Tk()
    root.title("Map drawing")
    root.geometry("{0}x{1}+0+0".format(
                    map.width + 1, map.height + 1))
    ex = Draw(map)

    root.mainloop()


map_drawing(Map(4, 7, 
            [[1,0,1,1,1,1,0], [1,0,0,0,0,0,0], [1,0,1,1,1,0,0], [0,0,1,0,0,0,0]], 
            (3, 0), (3, 3), 'RUURRRRDDLL'))