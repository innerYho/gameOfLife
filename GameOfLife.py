import pygame
import numpy as np
import time
pygame.init()

# Size
width, height = 1000, 1000

screen = pygame.display.set_mode((height, width))

#color background: almost black.
bg = 25, 25, 25
screen.fill(bg) # pass color value

#define the number of the cell (celda)
nxC, nyC = 25, 25

# width and height of the screen
dimCW = width / nxC
dimCH = height / nyC


#save the state
# life = 1 ; died = 0; 
gameState = np.zero((nxC, nyC))


#initial value 
    # branch bot
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1
    #Movil bot
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 21] = 1

#Execution Control of game
pauseExect = False

while True: 

    # Save in memory a copy of the gameState
    #save every update 
    newGameState = np.copy(gameState)


    #clean the screan for prevent the overPosition of life cell
    screen.fill(bg)
    #delay of time
    time.sleep(0.1)

    #Change the state of the cell with mouse and keyboard
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        #to know who key is pressed 
        mouseClick = pygame.mouse.get_pressed()
        # print(mouseClick)

# get the position in the screen that was selected
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            #round and convert to integer value
            celX, celY = int(np.floor(posX / dimCW), np.floor(posY / dimCH))
            # newGameState[celX, celY] = 1

#change for diferent value
            newGameState[celX, celY] = not mouseClick[2]

    #run the loop in axis x and axis y
    for y in range(0, nxC):
        for x in range(0, nyC):

# decide if the variable of game change or not
            if not pauseExect:

                #Calculate de number of neighbors 
                #if the cell life is in the border, it can display to other side od the screen 
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x) % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x) % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC] 

            #can be work in other game, when the neighbors is around the position selected
                # n_neigh = gameState[(x - 1), (y - 1)] + \
                #           gameState[(x), (y - 1)] + \
                #           gameState[(x + 1), (y - 1)] + \
                #           gameState[(x - 1), (y)] + \  
                #           gameState[(x + 1), (y)] + \
                #           gameState[(x - 1), (y + 1)] + \
                #           gameState[(x), (y + 1)] + \
                #           gameState[(x + 1), (y + 1)] 

        #Rule 1 : the cell died with 3 neighbors lifes can be reborn.
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1 

        #Rule 2 : one cell life with 2 or more neigbors died, it's died 
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0
            #Delimitar las coordenadas de los poligonos multiplicando los indices (ancho x alto)
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)
                    ]

                    #pasar los parametros de los cuadros en los que se va a colorear en gris
                    # border size: 1
            if newGameState[x, y] == 0:        
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1) #life
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0) #died

        #Update the state of the game.
        gameState = np.copy(newGameState)
    #show & uodate the frame in the screen
    pygame.display.flip()