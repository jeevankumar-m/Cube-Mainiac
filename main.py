import pygame, sys, random 
pygame.init() 
pygame.font.init() 
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

#font 
font = pygame.font.Font('pixel-operator.ttf', 12)
font2 = pygame.font.Font('pixel-operator.ttf', 30)
#music 
pygame.mixer.music.load('sfx/background.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

jump_sfx = pygame.mixer.Sound('sfx/jump.wav')
shoot_sfx = pygame.mixer.Sound('sfx/shoot.wav')

TILE_SIZE = dirt_img.get_width()

player_rect = pygame.Rect(0 * TILE_SIZE, 24 * TILE_SIZE, 16, 16)
enemy_rect = pygame.Rect(27 * TILE_SIZE, 26 * TILE_SIZE, player_img.get_width(), player_img.get_height())
background_objects = [[0.25,[120,10,40,500]],[0.25,[280,30,40,500]],[0.5,[30,40,40,500]],[0.5,[130,90,60,500]],[0.5,[400,80,60,500]]]
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

enemy_y_momentum = 0 
enemy_air_timer = 0 

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

jump = False 

shoot = False 
enemy_shoot = False
bullets = []
enemy_bullets = []


#alive logic 
enemy_alive = True
player_alive = True

#healthbar logic 
player_max_health = 100 
player_health = player_max_health 
enemy_max_health = 100 
enemy_health = enemy_max_health

#enemy spawns 
enemy_spawn = []
enemy_creation_count = 10
spawn_locs = []
for enemy_loc in range(enemy_creation_count):
    spawn_locs.append((random.randint(8, 95), random.randint(4, 30)))
for loc in spawn_locs:
    enemy_spawn.append((loc[0] * TILE_SIZE, loc[1] * TILE_SIZE))

current_spawn = 0 

kill_count = 0
kill_complete = False

def enemy_spawn_func(index):
    global enemy_alive, enemy_health
    enemy_rect.x, enemy_rect.y = enemy_spawn[index]
    enemy_alive = True 
    enemy_health = enemy_max_health

#States 
running = True
game_over = False 
winning = False
y_axis_shift = -20
playing = True 

normal_fill = (72, 77, 77)
game_over_fill = (0, 0, 0)
text_surf = font.render("HP", False, (255, 255, 255))
text_surf2 = font.render(str(kill_count) + "/" + str(enemy_creation_count) + " ENEMY KILLS", False, (255, 255, 255))
text_surf3 = font2.render("GAME OVER :(", False, (255, 13, 36))
text_surf4 = font2.render("YOU WON ;>", False, (95, 205, 228))

while running:
    if playing:
        if player_alive == True:
            display.fill(normal_fill)
        if player_alive != True:
            display.fill(game_over_fill)
        if winning:
            display.fill(game_over_fill)

        if player_alive:
            pygame.draw.rect(display, (43, 46, 46), pygame.Rect(0, 150, 350, 125))

        true_scroll[0] += (player_rect.x - true_scroll[0] - 175) / 5
        true_scroll[1] += (player_rect.y - true_scroll[1] - 125) / 5

        scroll = true_scroll.copy() 
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        if player_alive:
            for background_object in background_objects:
                obj_rect = pygame.Rect(background_object[1][0]-scroll[0] * background_object[0], background_object[1][1]-scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
                if background_object[0] == 0.5:   
                    surf = pygame.Surface((obj_rect.width, obj_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(surf, (33, 35, 35), (0, 0, obj_rect.width, obj_rect.height))
                else: 
                    surf = pygame.Surface((obj_rect.width, obj_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(surf, (14, 15, 15), (0, 0, obj_rect.width, obj_rect.height))
                rotated = pygame.transform.rotate(surf, -45)
                rot_rect = rotated.get_rect(center=obj_rect.center)
                display.blit(rotated, rot_rect)

        if not enemy_alive:
            current_spawn += 1
            if current_spawn < len(enemy_spawn):
                enemy_spawn_func(current_spawn)

        if kill_count == enemy_creation_count:
            kill_complete = True 

        if player_alive:
            player_bar_width = 50
            player_bar_height = 4 
            health_ratio = player_health / player_max_health
            current_width = player_bar_width * health_ratio 

            pygame.draw.rect(display, (60, 60, 60), pygame.Rect(25, 20, player_bar_width, player_bar_height))
            pygame.draw.rect(display, (40, 200, 40), pygame.Rect(25, 20, current_width, player_bar_height))
            pygame.draw.rect(display, (255, 255, 255), pygame.Rect(25, 20, player_bar_width, player_bar_height), 1)

        player_movement = [0, 0]
        if moving_right == True:
            player_movement[0] += 3
        if moving_left == True:
            player_movement[0] -= 3

        if enemy_cool_down_timer > 0:
            enemy_cool_down_timer -= 1

        enemy_movement = [0, 0]
        if enemy_alive:
            if enemy_moving_right == True:
                enemy_movement[0] += 1
            if enemy_moving_left == True:
                enemy_movement[0] -= 1

        if shoot == True:
            bullets.append([pygame.Rect(player_rect.x, player_rect.y, 5, 5), facing])
            shoot = False

        if enemy_alive and enemy_shoot == True:    
            if enemy_cool_down_timer == 0:
                shoot_sfx.set_volume(1)
                shoot_sfx.play()
                enemy_bullets.append([pygame.Rect(enemy_rect.x, enemy_rect.y, 5, 5), enemy_facing])
                enemy_cool_down_timer = 60 
                shoot = False

        enemy_moving_left = False
        enemy_moving_right = False

        enemy_movement[1] += enemy_y_momentum 
        enemy_y_momentum += 0.3

        #enemy chase logic
        if enemy_alive:
            if abs(player_rect.x - enemy_rect.x) < 150:
                if player_rect.x > enemy_rect.x:
                    enemy_moving_right = True 
                    enemy_shoot = True
                    enemy_facing = 1
                if player_rect.x < enemy_rect.x:
                    enemy_moving_left = True 
                    enemy_shoot = True
                    enemy_facing = -1

            if abs(player_rect.x - enemy_rect.x) < 5:
                enemy_moving_left = False
                enemy_moving_right = False

            if player_rect.y != enemy_rect.y:
                enemy_shoot = False

        if enemy_alive:
            enemy_bar_width = 16
            enemy_bar_height = 2
            health_ratio = enemy_health / enemy_max_health
            current_width = enemy_bar_width * health_ratio 

            pygame.draw.rect(display, (60, 60, 60), pygame.Rect(enemy_rect.x - scroll[0], enemy_rect.y - scroll[1] - 6, enemy_bar_width, enemy_bar_height))
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(enemy_rect.x - scroll[0], enemy_rect.y - scroll[1] - 6, current_width, enemy_bar_height))

        player_movement[1] += player_y_momentum 
        player_y_momentum += 0.2

        if player_movement[1] > 60:
            player_alive = False 

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
            pygame.draw.rect(display, (95, 205, 228), pygame.Rect(bullet_rect.x - scroll[0], (bullet_rect.y+5) - scroll[1], 5, 5))
            
            for tile in tile_rects:
                if bullet_rect.colliderect(tile):
                    bullets.remove(bullet)
                    break 
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    if enemy_health == 0:
                        enemy_alive = False
                        kill_count += 1
                    enemy_health -= 25
                    break

        for enemy_bullet in enemy_bullets:
            enemy_bullet_rect, enemy_bullet_direction = enemy_bullet
            enemy_bullet_rect.x += 6 * enemy_bullet_direction
            pygame.draw.rect(display, (255, 13, 36), pygame.Rect(enemy_bullet_rect.x - scroll[0], (enemy_bullet_rect.y+5) - scroll[1], 5, 5))
            
            for tile in tile_rects:
                if enemy_bullet_rect.colliderect(tile):
                    enemy_bullets.remove(enemy_bullet)
                if enemy_bullet_rect.colliderect(player_rect):
                    enemy_bullets.remove(enemy_bullet)
                    if player_health < 0:
                        player_alive = False
                    player_health -= 15
                    break 
        
        player_rect, collisions = move(player_rect, player_movement, tile_rects)
        enemy_rect, collisions_enemy = move(enemy_rect, enemy_movement, tile_rects)

        if player_rect.colliderect(game_over_rect[0]) and kill_complete == True:
            winning = True 

        if collisions['bottom']:
            player_y_momentum = 0 
            air_timer = 0 
        if collisions['top']:
            player_y_momentum = 1
        else:
            air_timer += 1


        if collisions_enemy['bottom']:
            enemy_y_momentum = 0
        if collisions_enemy['top']:
            enemy_y_momentum = 1

        if enemy_y_momentum > 100:
            enemy_rect.x = random.randint(8, 95)
            enemy_rect.y = random.randint(4, 30)

        if collisions_enemy['left']:
            enemy_y_momentum = -5
        if collisions_enemy['right']:
            enemy_y_momentum = - 5

        prev_player_rect = player_rect.copy() 

        if player_rect.colliderect(enemy_rect):

            dx = (player_rect.centerx - enemy_rect.centerx)
            dy = (player_rect.centery - enemy_rect.centery)
            overlap_x = (player_rect.width // 2 + enemy_rect.width // 2) - abs(dx)
            overlap_y = (player_rect.height // 2 + enemy_rect.height // 2) - abs(dy)
            if overlap_x < overlap_y:
                if dx > 0:
                    player_rect.left = enemy_rect.right
                else:
                    player_rect.right = enemy_rect.left

        display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        if enemy_alive:
            display.blit(enemy_img, (enemy_rect.x - scroll[0], enemy_rect.y - scroll[1]))

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
                jump = True 
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

    if player_alive == False:
        playing = False
    if winning == True:
        playing = False
    #font display 
    if playing == True and player_alive == True:
        display.blit(text_surf, (10, 15))
        display.blit(text_surf2, (230, 15))
    if player_alive != True and playing == False:
        if y_axis_shift < 110:
            display.fill((0, 0, 0))
            display.blit(text_surf3, (80, y_axis_shift))
            y_axis_shift += 2
        display.blit(text_surf3, (80, y_axis_shift))
    if player_alive == True and winning == True:
        if y_axis_shift < 110:
            display.fill((0, 0, 0))
            display.blit(text_surf4, (80, y_axis_shift))
            y_axis_shift += 2
        display.blit(text_surf4, (80, y_axis_shift))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() 
    clock.tick(60)