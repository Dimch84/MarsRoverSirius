import pygame

def map_drawing (n, m, map, start_point, finish_point, 
                mars_rover_path):

    if n == 0 or m == 0:
        print ("Error: invalid map size")
        return

    max_size_screen_side = 800
    size_cell = max_size_screen_side // max (n, m)

    # init screen 
    pygame.init()
    screen = pygame.display.set_mode((size_cell * m, size_cell * n))

    pygame.display.update()
    pygame.display.set_caption('Mars rover movement')
    
    # text style
    words_font = pygame.font.SysFont("comicsansms", 35)

    # color
    white = (255, 255, 255)
    red = (213, 50, 80)
    blue = (50, 153, 213)
    obstacle_color = (149, 163, 0)
    background_color = (241, 253, 114)
    text_color = (106, 35, 126)
    color_path = (187, 99, 212)

    
    #drawing screen
    show_screen = False
    while not show_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_screen = True
    
        # drawing map
        for i in range(n):
            for j in range (m):

                if map[i][j] == 1:
                    color = obstacle_color
                else:
                    color = background_color

                pygame.draw.rect(screen, color, [j * size_cell, i * size_cell,
                                 size_cell, size_cell])
        
        
        #out start and finish
        screen.blit(words_font.render("start", True, text_color),
                 dest = (size_cell * start_point[1], size_cell * start_point[0]))
        screen.blit(words_font.render("finish", True, text_color),
                 dest = (size_cell * finish_point[1], size_cell * finish_point[0]))


        # drawing movement Mars rover
        mars_rover_coordinate_y = start_point[0]
        mars_rover_coordinate_x = start_point[1]
        for step in mars_rover_path:
            
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

            pygame.draw.line(screen, color_path, 
                            (mars_rover_coordinate_x * size_cell + size_cell // 2,
                            mars_rover_coordinate_y * size_cell + size_cell // 2),
                            (new_mars_rover_coordinate_x * size_cell + size_cell // 2,
                            new_mars_rover_coordinate_y * size_cell + size_cell // 2),
                            5)


            mars_rover_coordinate_x = new_mars_rover_coordinate_x
            mars_rover_coordinate_y = new_mars_rover_coordinate_y


        pygame.display.update()

    pygame.quit()
    quit()


# exemple
map_drawing(4, 7, 
            [[1,0,1,1,1,1,0], [1,0,0,0,0,0,0], [1,0,1,1,1,0,0], [0,0,1,0,0,0,0]], 
            (3, 0), (3, 3), 'RUURRRRDDLL')