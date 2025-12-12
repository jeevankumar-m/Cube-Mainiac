import pygame, sys
pygame.init() 
from pygame.locals import * 

pygame.display.set_caption('Cube Mainiac')
WINDOW_SIZE = (700, 500)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((350, 250))

clock = pygame.time.Clock() 

player_img = pygame.image.load('player.png') 
dirt_img = pygame.image.load('dirt.png')

TILE_SIZE = dirt_img.get_width()

player_y_momentum = 0
player_movement = [50, 50]
moving_right = False 
moving_left = False 

while True:
    display.fill((255, 255, 255))


    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2

    player_movement[1] += player_y_momentum 
    player_y_momentum += 0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True 
            if event.key == K_LEFT:
                moving_left = True 
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False 
            if event.key == K_LEFT:
                moving_left = False 

    display.blit(player_img, (player_movement[0], player_movement[1]))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() 
    clock.tick(60)