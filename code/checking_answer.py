from map import Map

def checking_the_answer_simple_map(map : Map) -> bool:
    
    mars_rover_y = map.start_point[0]
    mars_rover_x = map.start_point[1]
    
    for step in map.mars_rover_path:
        
        if step == 'U':
            mars_rover_y -= 1
        if step == 'D':
            mars_rover_y += 1
        if step == 'R':
            mars_rover_x += 1
        if step == 'L':
            mars_rover_x -= 1
        
        # out-of-bounds check
        if (mars_rover_x < 0 or mars_rover_x >= map.m
            or mars_rover_y < 0 or mars_rover_y >= map.n):
            return False

        # walking test
        if (map.map[mars_rover_y][mars_rover_x] == 1):
            return False

    # checking that they came to the right place
    if (map.finish_point != (mars_rover_x, mars_rover_y)):
        return False
    
    return True