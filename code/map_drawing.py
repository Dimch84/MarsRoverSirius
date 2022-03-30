import pygame


def map_drawing (n, m, map, start_point, finish_point, 
                robot_path):

    if n == 0 or m == 0:
        print ("Error: invalid map size")
        return

    max_size_dis_side = 800
    size_cell = max_size_dis_side // max (n, m)

    print (size_cell, n, m)

    pygame.init()
    dis = pygame.display.set_mode((size_cell * m, size_cell * n))

    pygame.display.update()
    pygame.display.set_caption('Mars Rover movement')

    blue = (0, 0, 255)
    white = (255, 255, 255)

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
    
        for i in range(n):
            for j in range (m):

                if map[i][j] == 1:
                    color = blue
                else:
                    color = white

                pygame.draw.rect(dis, color, [j * size_cell, i * size_cell,
                                 size_cell, size_cell])
        
        pygame.display.update()

    pygame.quit()
    quit()


