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

player_rect = pygame.Rect(100, 100, player_img.get_width(), player_img.get_height())
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close() 
    data = data.split('\n')
    game_map = [] 
    for row in data:
        game_map.append(list(row))
    return game_map 

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list 

def move(rect, movement, tiles):
    collision_types = {'top':False, 'bottom':False, 'left':False, 'right':False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left 
            collision_types['right'] = True
        if movement[0] < 0:
            rect.left = tile.right 
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] < 0:
            rect.top = tile.bottom 
            collision_types['top'] = True
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
    return rect, collision_types

game_map = load_map('map')
player_y_momentum = 0

moving_right = False 
moving_left = False 
true_scroll = [0, 0]


while True:
    display.fill((255, 255, 255))

    true_scroll[0] += (player_rect.x - true_scroll[0] - 191) / 20 
    true_scroll[1] += (player_rect.y - true_scroll[1] - 141) / 20 

    scroll = true_scroll.copy() 
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2

    player_movement[1] += player_y_momentum 
    player_y_momentum += 0.2

    tile_rects = []
    y = 0 
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1': 
                display.blit(dirt_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(dirt_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1 
        y += 1

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True 
            if event.key == K_LEFT:
                moving_left = True 
            if event.key == K_UP:
                player_y_momentum = -5 
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False 
            if event.key == K_LEFT:
                moving_left = False 

    display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() 
    clock.tick(60)