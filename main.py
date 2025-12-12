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

#music 
pygame.mixer.music.load('sfx/background.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

jump_sfx = pygame.mixer.Sound('sfx/jump.wav')
shoot_sfx = pygame.mixer.Sound('sfx/shoot.wav')

TILE_SIZE = dirt_img.get_width()

player_rect = pygame.Rect(0 * TILE_SIZE, 24 * TILE_SIZE, player_img.get_width(), player_img.get_height())
enemy_rect = pygame.Rect(27 * TILE_SIZE, 26 * TILE_SIZE, player_img.get_width(), player_img.get_height())
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
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
facing = 1 #for left side it is -1 
enemy_facing = 1
enemy_cool_down_timer = 0 

shoot = False 
enemy_shoot = False
bullets = []
enemy_bullets = []

running = True
while running:
    display.fill((72, 77, 77))
    pygame.draw.rect(display, (43, 46, 46), pygame.Rect(0, 150, 350, 125))

    true_scroll[0] += (player_rect.x - true_scroll[0] - 191) / 20 
    true_scroll[1] += (player_rect.y - true_scroll[1] - 141) / 20 

    scroll = true_scroll.copy() 
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0] * background_object[0], background_object[1][1]-scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (33, 35, 35), obj_rect)
        else:
            pygame.draw.rect(display, (14, 15, 15), obj_rect)

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 3
    if moving_left == True:
        player_movement[0] -= 3

    if enemy_cool_down_timer > 0:
        enemy_cool_down_timer -= 1

    enemy_movement = [0, 0]
    if enemy_moving_right == True:
        enemy_movement[0] += 1
    if enemy_moving_left == True:
        enemy_movement[0] -= 1

    if shoot == True:
        bullets.append([pygame.Rect(player_rect.x, player_rect.y, 5, 5), facing])
        shoot = False

    if enemy_shoot == True:
        
        if enemy_cool_down_timer == 0:
            shoot_sfx.set_volume(1)
            shoot_sfx.play()
            enemy_bullets.append([pygame.Rect(enemy_rect.x, enemy_rect.y, 5, 5), facing])
            enemy_cool_down_timer = 60 
            shoot = False

    enemy_moving_left = False
    enemy_moving_right = False

    #enemy chase logic
    if abs(player_rect.x - enemy_rect.x) < 100:
        if player_rect.x > enemy_rect.x and player_rect.y == enemy_rect.y:
            enemy_moving_right = True 
            enemy_shoot = True
            enemy_facing = 1
        if player_rect.x < enemy_rect.x and player_rect.y == enemy_rect.y:
            enemy_moving_left = True 
            enemy_shoot = True
            enemy_facing = -1

    if abs(player_rect.x - enemy_rect.x) < 5:
        enemy_moving_left = False
        enemy_moving_right = False

    if player_rect.y != enemy_rect.y:
        enemy_shoot = False

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
        bullet_rect, direction = bullet
        bullet_rect.x += 10 * direction
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(bullet_rect.x - scroll[0], (bullet_rect.y+5) - scroll[1], 5, 5))
        
        for tile in tile_rects:
            if bullet_rect.colliderect(tile):
                bullets.remove(bullet)
                break 

    for enemy_bullet in enemy_bullets:
        enemy_bullet_rect, enemy_bullet_direction = enemy_bullet
        enemy_bullet_rect.x += 6 * enemy_bullet_direction
        pygame.draw.rect(display, (0, 255, 0), pygame.Rect(enemy_bullet_rect.x - scroll[0], (enemy_bullet_rect.y+5) - scroll[1], 5, 5))
        
        for tile in tile_rects:
            if enemy_bullet_rect.colliderect(tile):
                enemy_bullets.remove(enemy_bullet)
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
                facing = 1
            if event.key == K_LEFT:
                moving_left = True 
                facing = -1
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
                    jump_sfx.play()
                    jump_sfx.set_volume(1)
            if event.key == K_SPACE:
                shoot = True 
                shoot_sfx.play()
                shoot_sfx.set_volume(1)
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