from tkinter import *

from code.map import Map
from map_editor.square import SquareType, SquareTypeName, SquareTypeColor
from code.color_application import color

MINIMUM_CELL_SIZE_FOR_IMAGE = 50

class draw(Frame):
 
    def __init__(self, master, map : Map, files_name):
        self.slave = Toplevel(master)
        self.slave.title('Map drawing')
        self.slave.geometry("{0}x{1}+0+0".format(
                           map.width + 300, map.height + 1))

        super().__init__()
        self.initUI(map, files_name)

    def initUI(self, map : Map, files_name) -> None:

        canvas = Canvas(self.slave)
        canvas.pack(fill = 'both', expand = 1)

        self.draw_map (map, canvas)
        for i in range(len(map.mars_rover_paths)):
            self.draw_path (map, canvas, i)
        self.draw_start_and_finish (map, canvas)
        self.color_paths (map, canvas, files_name)

        if map.radius == -1:
            self.animation (map, canvas)
        else:
            self.animation_with_dawn (map, canvas)

    def draw_path (self, map : Map, canvas : Canvas, index : int) -> None:
        
        # drawing movement Mars rover
        mars_rover_coordinate_y = map.start_point[0]
        mars_rover_coordinate_x = map.start_point[1]
        for step in map.mars_rover_paths[index]:

            new_mars_rover_coordinate_y = mars_rover_coordinate_y
            new_mars_rover_coordinate_x = mars_rover_coordinate_x
            
            new_mars_rover_coordinate_x += step[1]
            new_mars_rover_coordinate_y += step[0]


            canvas.create_line(
                            mars_rover_coordinate_x * map.size_cell + map.size_cell // 2,
                            mars_rover_coordinate_y * map.size_cell + map.size_cell // 2,
                            new_mars_rover_coordinate_x * map.size_cell + map.size_cell // 2,
                            new_mars_rover_coordinate_y * map.size_cell + map.size_cell // 2,
                            arrow = 'last',
                            dash = (5, 2),
                            fill = color.color_paths[min(index, len(color.color_paths) - 1)])



            mars_rover_coordinate_x = new_mars_rover_coordinate_x
            mars_rover_coordinate_y = new_mars_rover_coordinate_y

    def draw_start_and_finish (self, map : Map, canvas : Canvas) -> None:

        #out start and finish
        canvas.create_text(map.size_cell * map.start_point[1] + map.size_cell // 2, 
                            map.size_cell * map.start_point[0] + map.size_cell // 2,
                            text = 'START',
                            justify = 'center')
        canvas.create_text(map.size_cell * map.finish_point[1] + map.size_cell // 2, 
                            map.size_cell * map.finish_point[0] + map.size_cell // 2,
                            text = 'FINISH',
                            justify = 'center')

    def draw_map (self, map : Map, canvas : Canvas) -> None:

        for i in range (map.m):
            for j in range (map.n):

                color_cell = SquareTypeColor[SquareType(int(map.map[j][i]))]

                canvas.create_rectangle(
                        map.size_cell * i, map.size_cell * j,
                        map.size_cell * (i + 1), map.size_cell * (j + 1),
                        outline = 'black', fill = color_cell, width = 1)

    def animation (self, map : Map, canvas : Canvas) -> None:
        
        mars_rover_coordinate_y = mars_rover_coordinate_x = 1

        img_rover = PhotoImage(file = "images/mars_rover.png")
        rover = canvas.create_image(
                                        map.start_point[1] * map.size_cell + 
                                        map.size_cell // 2,
                                        map.start_point[0] * map.size_cell + 
                                        map.size_cell // 2, 
                                        anchor = CENTER, 
                                        image = img_rover)
        
        if map.size_cell < MINIMUM_CELL_SIZE_FOR_IMAGE:
            rover = canvas.create_rectangle(map.start_point[1] * map.size_cell + 
                                            map.size_cell // 4, 
                                            map.start_point[0] * map.size_cell + 
                                            map.size_cell // 4,
                                            (map.start_point[1] + 1) * map.size_cell - 
                                            map.size_cell // 4,
                                            (map.start_point[0] + 1) * map.size_cell -
                                            map.size_cell // 4,
                                            outline = 'black', 
                                            fill = 'black', 
                                            width = 1)

        

        for step in map.mars_rover_paths[0]:

            mars_rover_coordinate_x = step[1] 
            mars_rover_coordinate_y = step[0]

            #animation
            for i in range (map.size_cell):

                canvas.move(rover, 
                            mars_rover_coordinate_x, 
                            mars_rover_coordinate_y)
                self.update()
                canvas.after(3000 // (map.size_cell * len(map.mars_rover_paths[0])))

    def animation_with_dawn (self, map : Map, canvas : Canvas) -> None:
        
        mars_rover_coordinate_y = mars_rover_coordinate_x = 1


        img_rover = PhotoImage(file = "images/mars_rover.png")
        rover = canvas.create_image(
                                        map.start_point[1] * map.size_cell + 
                                        map.size_cell // 2,
                                        map.start_point[0] * map.size_cell + 
                                        map.size_cell // 2, 
                                        anchor = CENTER, 
                                        image = img_rover)
        
        if map.size_cell < MINIMUM_CELL_SIZE_FOR_IMAGE:
            rover = canvas.create_rectangle(map.start_point[1] * map.size_cell + 
                                            map.size_cell // 4, 
                                            map.start_point[0] * map.size_cell + 
                                            map.size_cell // 4,
                                            (map.start_point[1] + 1) * map.size_cell - 
                                            map.size_cell // 4,
                                            (map.start_point[0] + 1) * map.size_cell -
                                            map.size_cell // 4,
                                            outline = 'black', 
                                            fill = 'black', 
                                            width = 1)

        # black_zone
        black_lines = []
        
        for x in range (-map.m, 2 * map.m):
            for y in range (-map.n, 2 * map.n):
                if max(abs(x - map.start_point[1]), abs(y - map.start_point[0])) > map.radius:
                    black_lines.append(
                        canvas.create_rectangle(
                                x * map.size_cell,
                                y * map.size_cell,
                                (x + 1) * map.size_cell,
                                (y + 1) * map.size_cell,
                                fill = 'black',
                                ))

        for step in map.mars_rover_paths[0]:
            
            mars_rover_coordinate_x = step[1] 
            mars_rover_coordinate_y = step[0]

            #animation
            for i in range (map.size_cell):

                canvas.move(rover, 
                            mars_rover_coordinate_x, 
                            mars_rover_coordinate_y)

                for black_line in black_lines: 
                    canvas.move(black_line,
                                mars_rover_coordinate_x, 
                                mars_rover_coordinate_y)

                self.update()
                canvas.after(3000 // (map.size_cell * len(map.mars_rover_paths[0])))

    def color_paths (self, map : Map, canvas : Canvas, files_name) -> None:

        for i in range(len(map.mars_rover_paths)):
            y = 25 + 20 * i,
            canvas.create_line(
                            map.width + 10, y,
                            map.width + 50, y,
                            arrow = 'last',
                            dash = (5, 2),
                            fill = color.color_paths[min(i, len(color.color_paths) - 1)])

            canvas.create_text(
                            map.width + 75, y,
                            text = str(len(map.mars_rover_paths[i])),
                            justify = 'left')

            canvas.create_text(
                            map.width + 200, y,
                            text = files_name[i].split('/')[-1],
                            justify = 'center')