
class Map:

    max_size_screen_side = 800
    radius = 2

    def __init__(self, 
                 n: int, m: int, map: list,
                 start_point: list, finish_point: list, 
                 mars_rover_path: str):
        
        self.n = n
        self.m = m
        self.map = map
        self.start_point = start_point
        self.finish_point = finish_point
        self.mars_rover_path = mars_rover_path

        self.size_cell = self.max_size_screen_side // max (n, m)
        self.height = self.size_cell * n
        self.width = self.size_cell * m

    