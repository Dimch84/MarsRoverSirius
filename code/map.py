
class Map:

    """
    This is the map class
    :param radius: if it equals -1,
                then the normal mode works 
                where the entire map is visible, 
                otherwise the mode with a black zone is switched on,
                where it is visible only within the visibility radius.
    """

    max_size_screen_side = 800
    radius = -1

    def __init__(self, 
                 n: int, m: int, map: list,
                 start_point: list, finish_point: list, 
                 mars_rover_paths: list,
                 radius_black_zone: int):
        
        self.n = n
        self.m = m
        self.map = map
        self.start_point = start_point
        self.finish_point = finish_point
        self.mars_rover_paths = mars_rover_paths
        self.radius = radius_black_zone

        self.size_cell = self.max_size_screen_side // max (n, m)
        self.height = self.size_cell * n
        self.width = self.size_cell * m
