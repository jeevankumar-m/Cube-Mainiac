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
dirt2_img = pygame.image.load('dirt2.png')
game_over_img = pygame.image.load('gameover.png')
enemy_img = pygame.image.load('enemy.png')

TILE_SIZE = dirt_img.get_width()

player_rect = pygame.Rect(0 * TILE_SIZE, 24 * TILE_SIZE, player_img.get_width(), player_img.get_height())
enemy_rect = pygame.Rect(27 * TILE_SIZE, 26 * TILE_SIZE, player_img.get_width(), player_img.get_height())
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

#if distance between the x of player and x of enemy in a range 
#if player.x > enemy.x 
#then enemy.x += 2 
#is player.x < enemy.x 
#then enemy.x -= 2

game_map = load_map('map')
player_y_momentum = 0
air_timer = 0 

moving_right = False 
moving_left = False 
true_scroll = [0, 0]

enemy_moving_left = False 
enemy_moving_right = False 

shoot = False 
bullets = []

running = True
while running:
    display.fill((72, 77, 77))
    pygame.draw.rect(display, (43, 46, 46), pygame.Rect(0, 150, 350, 125))

    true_scroll[0] += (player_rect.x - true_scroll[0] - 191) / 20 
    true_scroll[1] += (player_rect.y - true_scroll[1] - 141) / 20 

    scroll = true_scroll.copy() 
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 3
    if moving_left == True:
        player_movement[0] -= 3

    enemy_movement = [0, 0]
    if enemy_moving_right == True:
        enemy_movement[0] += 2
    if enemy_moving_left == True:
        enemy_movement[0] -= 2

    if shoot == True:
        bullets.append(pygame.Rect(player_rect.x, player_rect.y, 5, 5))
        shoot = False

    enemy_moving_left = False
    enemy_moving_right = False

    if abs(player_rect.x - enemy_rect.x) < 100:
        if player_rect.x > enemy_rect.x:
            enemy_moving_right = True 
        if player_rect.x < enemy_rect.x:
            enemy_moving_left = True 

    if abs(player_rect.x - enemy_rect.x) < 5:
        enemy_moving_left = False
        enemy_moving_right = False

    player_movement[1] += player_y_momentum 
    player_y_momentum += 0.2

    tile_rects = []
    game_over_rect = []
    y = 0 
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1': 
                display.blit(dirt_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(dirt2_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '3':
                display.blit(game_over_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                game_over_rect.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile != '0' and tile != '3':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1 
        y += 1

    for bullet in bullets:
        bullet.x += 10  
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(bullet.x - scroll[0], (bullet.y+5) - scroll[1], 5, 5))
        
        for tile in tile_rects:
            if bullet.colliderect(tile):
                bullets.remove(bullet)
                break 

    
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    enemy_rect, collisions_enemny = move(enemy_rect, enemy_movement, tile_rects)

    if player_rect.colliderect(game_over_rect[0]):
        running = False

    if collisions['bottom']:
        player_y_momentum = 0 
        air_timer = 0 
    if collisions['top']:
        player_y_momentum = 1
    else:
        air_timer += 1
    
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
                if air_timer < 6:
                    player_y_momentum = -5
            if event.key == K_SPACE:
                shoot = True 
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False 
            if event.key == K_LEFT:
                moving_left = False 

    display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    display.blit(enemy_img, (enemy_rect.x - scroll[0], enemy_rect.y - scroll[1]))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() 
    clock.tick(60)