import pygame

def map_drawing (n, m, map, start_point, finish_point, 
                robot_path):

    if n == 0 or m == 0:
        print ("Error: invalid map size")
        return

    max_size_screen_side = 800
    size_cell = max_size_screen_side // max (n, m)

    # init screen 
    pygame.init()
    screen = pygame.display.set_mode((size_cell * m, size_cell * n))

    pygame.display.update()
    pygame.display.set_caption('Mars Rover movement')
    
    # text style
    words_font = pygame.font.SysFont("comicsansms", 35)

    # color
    white = (255, 255, 255)
    red = (213, 50, 80)
    blue = (50, 153, 213)
    obstacle_color = blue
    background_color = white
    text_color = red

    
    # drawing map
    show_screen = False
    while not show_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_screen = True
    
        for i in range(n):
            for j in range (m):

                if map[i][j] == 1:
                    color = obstacle_color
                else:
                    color = background_color

                pygame.draw.rect(screen, color, [j * size_cell, i * size_cell,
                                 size_cell, size_cell])
        
        
        screen.blit(words_font.render("start", True, text_color),
                 dest = (size_cell * start_point[1], size_cell * start_point[0]))
        screen.blit(words_font.render("finish", True, text_color),
                 dest = (size_cell * finish_point[1], size_cell * finish_point[0]))

        pygame.display.update()

    pygame.quit()
    quit()


