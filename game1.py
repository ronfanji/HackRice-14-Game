import pygame
from sys import exit
import math
from settings import *

pygame.init()

# Game Setup
WIDTH = 1500
HEIGHT = 750
FPS = 60
BLOCK_SIZE = 50


# Player Settings
PLAYER_START_X = WIDTH//2
PLAYER_START_Y = HEIGHT//2
PLAYER_SIZE = 1 #0.2
PLAYER_SPEED = 5

# Enemy Settings
ENEMY_SPEED = 1

# Bullet Settings
SHOOT_COOLDOWN = 20
BULLET_SCALE = 1 #0.1 
BULLET_SPEED = 10
BULLET_LIFETIME = 250

# Block Settings
BLOCK_LIFETIME = 800
BLOCK_COOLDOWN = 50
BLOCK_SCALE = 1
BLOCK_SPEED = PLAYER_SPEED



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RADish BEETS 'em Up")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("dirt.png").convert(), (WIDTH, HEIGHT))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.scale(pygame.image.load("radish_not_png.jpg").convert(), (BLOCK_SIZE, BLOCK_SIZE))
        #self.image = pygame.transform.rotozoom(pygame.image.load("radish_not_png.jpg").convert_alpha(), 0, PLAYER_SIZE) # change later
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.block = False
        self.block_cooldown = 0

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        current_dir = [1, 0]
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
            current_dir[0] = 0
            current_dir[1] = -1
        elif keys[pygame.K_s]:
            self.velocity_y = self.speed
            current_dir[0] = 0
            current_dir[1] = 1
        elif keys[pygame.K_d]:
            self.velocity_x = self.speed
            current_dir[0] = 1
        elif keys[pygame.K_a]:
            self.velocity_x = -self.speed
            current_dir[0] = -1

        
        if keys[pygame.K_SPACE]:
            self.shoot = True 
            self.is_shooting(current_dir)
        else:
            self.shoot = False

        if keys[pygame.K_p]:
            self.block = True 
            self.is_blocking(current_dir)
        else:
            self.block = False


        # Move the player temporarily
        temp_rect = self.rect.move(self.velocity_x, self.velocity_y)

        # Check for collisions
        for block_x in range(len(block_list)):
            for block_y in range(len(block_list[0])):
                if block_list[block_x][block_y] == 1:
                    block_rect = pygame.Rect(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

                    if temp_rect.colliderect(block_rect):
                        # Handle collision response
                        if self.velocity_y < 0:  # Moving up
                            temp_rect.top = block_rect.bottom
                            self.pos += pygame.math.Vector2(self.velocity_x, 0)
                        elif self.velocity_y > 0:  # Moving down
                            temp_rect.bottom = block_rect.top
                            self.pos += pygame.math.Vector2(self.velocity_x, 0)
                        elif self.velocity_x < 0:  # Moving left
                            temp_rect.left = block_rect.right
                            self.pos += pygame.math.Vector2(0, self.velocity_y)
                        elif self.velocity_x > 0:  # Moving right
                            temp_rect.right = block_rect.left
                            self.pos += pygame.math.Vector2(0, self.velocity_y)

        # Update the player's rectangle position
        self.rect = temp_rect
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)


    def attack(self):
        keys = pygame.key.get_pressed()

    def update(self):
        self.user_input()
        # self.move()
        self.attack()



    def is_shooting(self, dir): 
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos

            for i in range(3):
                if dir[0] == -1:
                    self.bullet = Bullet(spawn_bullet_pos[0] - (i+1)*BLOCK_SIZE, spawn_bullet_pos[1] - BLOCK_SIZE//2, dir)
                elif dir[0] == 1:
                    self.bullet = Bullet(spawn_bullet_pos[0] + i*BLOCK_SIZE, spawn_bullet_pos[1] - BLOCK_SIZE//2, dir)
                elif dir[1] == -1:
                    self.bullet = Bullet(spawn_bullet_pos[0]- BLOCK_SIZE//2, spawn_bullet_pos[1] - (i+1)*BLOCK_SIZE, dir)
                elif dir[1] != 0:
                    self.bullet = Bullet(spawn_bullet_pos[0]- BLOCK_SIZE//2, spawn_bullet_pos[1] + i*BLOCK_SIZE, dir)
                bullet_group.add(self.bullet)
                all_sprites_group.add(self.bullet)
    
    def is_blocking(self, dir): 
        if self.block_cooldown == 0:
            self.block_cooldown = BLOCK_COOLDOWN
            spawn_block = self.pos
            surrounding = [(-1, -1),(-1, 0),(-1, 1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for sur_block in surrounding:
                self.block = Block(spawn_block[0] + sur_block[0]*BLOCK_SIZE - BLOCK_SIZE//2, spawn_block[1] + sur_block[1]*BLOCK_SIZE - BLOCK_SIZE//2, dir)
                block_group.add(self.block)
                all_sprites_group.add(self.block)

                grid_row = math.floor(spawn_block[0] + sur_block[0]*BLOCK_SIZE - BLOCK_SIZE//2)//BLOCK_SIZE
                grid_col = math.floor(spawn_block[1] + sur_block[1]*BLOCK_SIZE - BLOCK_SIZE//2)//BLOCK_SIZE
                block_list[grid_row][grid_col] = 1


    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

        # boundary
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WIDTH - self.image.get_width():
            self.pos.x = WIDTH - self.image.get_width()

        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > HEIGHT - self.image.get_height():
            self.pos.y = HEIGHT - self.image.get_height()

        self.rect.center = self.pos

    def update(self):
        self.user_input()
        self.move()
        

        self.attack()
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.block_cooldown > 0:
            self.block_cooldown -= 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("radish_not_png.jpg").convert(), (BLOCK_SIZE, BLOCK_SIZE))
        
        #self.image = pygame.image.load("radish_not_png.jpg").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED

        self.x_vel = dir[0] * self.speed
        self.y_vel = dir[1] * self.speed
        
        
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()



    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("radish_not_png.jpg").convert(), (BLOCK_SIZE, BLOCK_SIZE))
        
        #self.image = pygame.image.load("radish_not_png.jpg").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BLOCK_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        
        self.block_lifetime = BLOCK_LIFETIME
        self.spawn_time = pygame.time.get_ticks()



    def block_wall(self):

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.block_lifetime:
            print(self.x, self.y)
            
            grid_row = math.floor(self.x / BLOCK_SIZE)
            grid_col = math.floor(self.y / BLOCK_SIZE)
            print (block_list[grid_row][grid_col])
            print(block_list)
            block_list[grid_row][grid_col] = 0
            self.kill()

    def update(self):
        self.block_wall()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load("enemy_not_png.jpg").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.125)

        self.rect = self.image.get_rect(center = position)
        self.speed = ENEMY_SPEED

        #self.position = pygame.math.Vector2(position)

    def follow_player(self):
        player_vector = pygame.math.Vector2(player.pos)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.distance(player_vector, enemy_vector)


        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
            self.rect.center += self.direction * self.speed
 
        else:
            self.direction = pygame.math.Vector2()

    def distance(self, vector1, vector2):
        return (vector1 - vector2).magnitude()
    
    def update(self):
        self.follow_player()

all_sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Player()
enemy = Enemy((300, 300))

bullet_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()

all_sprites_group.add(player)
all_sprites_group.add(enemy)

block_list = []
for i in range(WIDTH // BLOCK_SIZE):
    temp_block_list = []
    for j in range(HEIGHT // BLOCK_SIZE):
        temp_block_list.append(0)
    block_list.append(temp_block_list)

game_over = False

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not game_over:
        screen.blit(background, (0, 0))

        
        all_sprites_group.draw(screen)
        all_sprites_group.update()

        if pygame.sprite.collide_rect(player,enemy):
            game_over = False

    
    # screen.blit(player.image, player.pos)
    # player.update()

    pygame.display.update()
    clock.tick(FPS)