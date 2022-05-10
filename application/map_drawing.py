from tkinter import *

from application.map import Map

class draw(Frame):
 
    def __init__(self, master, map : Map):
        self.slave = Toplevel(master)
        self.slave.title('Map drawing')
        self.slave.geometry("{0}x{1}+0+0".format(
                           map.width + 1, map.height + 1))

        super().__init__()
        self.initUI(map)

    def initUI(self, map : Map) -> None:

        canvas = Canvas(self.slave)
        canvas.pack(fill = 'both', expand = 1)

        self.draw_map (map, canvas)
        self.draw_path (map, canvas)

        if map.radius == -1:
            self.animation (map, canvas)
        else:
            self.animation_with_dawn (map, canvas)

    
    def draw_path (self, map : Map, canvas : Canvas) -> None:
        
        # drawing movement Mars rover
        mars_rover_coordinate_y = map.start_point[0]
        mars_rover_coordinate_x = map.start_point[1]
        for step in map.mars_rover_path:

            new_mars_rover_coordinate_y = mars_rover_coordinate_y
            new_mars_rover_coordinate_x = mars_rover_coordinate_x
            
            # next coordinate
            # if step == 'U':
            #     new_mars_rover_coordinate_y -= 1
            # if step == 'D':
            #     new_mars_rover_coordinate_y += 1
            # if step == 'R':
            #     new_mars_rover_coordinate_x += 1
            # if step == 'L':
            #     new_mars_rover_coordinate_x -= 1

            new_mars_rover_coordinate_x += step[1]
            new_mars_rover_coordinate_y += step[0]


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

    def draw_map (self, map : Map, canvas : Canvas) -> None:
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

    def animation (self, map : Map, canvas : Canvas) -> None:
        
        mars_rover_coordinate_y = mars_rover_coordinate_x = 1

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

        

        for step in map.mars_rover_path:

            mars_rover_coordinate_x = step[1] 
            mars_rover_coordinate_y = step[0]

            #animation
            for i in range (map.size_cell):

                canvas.move(rover, 
                            mars_rover_coordinate_x, 
                            mars_rover_coordinate_y)
                self.update()
                canvas.after(3000 // (map.size_cell * len(map.mars_rover_path)))

    def animation_with_dawn (self, map : Map, canvas : Canvas) -> None:
        
        mars_rover_coordinate_y = mars_rover_coordinate_x = 1

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
                if abs(x - map.start_point[1]) + abs(y - map.start_point[0]) > map.radius:
                    black_lines.append(
                        canvas.create_rectangle(
                                x * map.size_cell,
                                y * map.size_cell,
                                (x + 1) * map.size_cell,
                                (y + 1) * map.size_cell,
                                fill = 'black',
                                ))

        for step in map.mars_rover_path:
            
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
                canvas.after(3000 // (map.size_cell * len(map.mars_rover_path)))

