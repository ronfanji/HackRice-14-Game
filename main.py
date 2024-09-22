# import necessary modules
import pygame
import sys
import random

pygame.mixer.init()

# define game variables
# Example: 24*16 grid
X = 12
Y = 8
side_len = 100
num_chase_enemy = 3
num_random_enemy = 2
soil_rate = 0.5
enemy_movement_rate = 0.9
enemy_moving_period = 50
BULLET_SPEED = 10
BULLET_LIFETIME = 500
SHOOT_COOLDOWN = 2

MENU, GAMEPLAY, GAME_OVER, VICTORY = 0, 1, 2, 3
current_state = 0

num_enemy = num_chase_enemy + num_random_enemy
width = X * side_len
height = Y * side_len

# initialize screen display with width and height 
screen = pygame.display.set_mode((width, height))

# set the current screen caption
pygame.display.set_caption("Raddish")

# create an object to help track time
clock = pygame.time.Clock()

# load images

starting_img = pygame.image.load('RADish_background.png').convert_alpha()
starting_img = pygame.transform.scale(starting_img, (X*side_len,Y*side_len))

ending_img = pygame.image.load('GAMEOVER_SCREEN.png').convert_alpha()
ending_img = pygame.transform.scale(ending_img, (X*side_len, Y*side_len))

soil_img = pygame.image.load('soil.png').convert_alpha()
soil_img = pygame.transform.scale(soil_img, (side_len, side_len))
grass_img = pygame.image.load('obstacle_soil.png').convert_alpha()
grass_img = pygame.transform.scale(grass_img, (side_len, side_len))

raddish_imgs = []
for i in range(12):
    imgName = 'character_'+str(i)+'.png'
    img = pygame.image.load(imgName).convert_alpha()
    img = pygame.transform.scale(img, (side_len, int(side_len/32*36)))
    raddish_imgs.append(img)

angry_imgs = []
for i in range(12):
    imgName = 'angry_'+str(i)+'.png'
    img = pygame.image.load(imgName).convert_alpha()
    img = pygame.transform.scale(img, (side_len, int(side_len/32*36)))
    angry_imgs.append(img)

enemy_img = pygame.image.load('enemy.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (side_len, side_len))

# everything about the raddish
class Raddish(object):
    def __init__(self, x, y, status, color=1):
        self.x = x
        self.y = y
        self.status = status
        self.color = color
        self.shoot = False
        self.shoot_cooldown = 0


    def draw(self):
        self.w, self.h = raddish_imgs[self.status].get_size()
        if self.color == 1:
            screen.blit(raddish_imgs[self.status], ((self.x+1)*side_len-self.w, (self.y+1)*side_len-self.h))
        else:
            screen.blit(angry_imgs[self.status], ((self.x+1)*side_len-self.w, (self.y+1)*side_len-self.h))
    
    def move(self, direction):
        dx, dy = 0, 0
        if direction == 0:
            dy = 1
        elif direction == 3:
            dx = 1
        elif direction == 6:
            dy = -1
        elif direction == 9:
            dx = -1
        tx, ty = self.x+dx, self.y+dy
        if self.status != direction:
            self.status = direction
        else:
            if tx>=0 and tx<X and ty>=0 and ty<Y and grid[tx][ty].status == 1:
                self.x, self.y = tx, ty

    def is_shooting(self, dir):
        if self.shoot_cooldown == 0:
            
            xsf = pygame.mixer.Sound('throw.mp3')
            pygame.mixer.Sound.set_volume(xsf, 0.5)
            pygame.mixer.Sound.play(xsf)
            
            self.shoot_cooldown = SHOOT_COOLDOWN

            if dir == 9:
                self.bullet = Bullet(self.x*side_len + side_len//2, self.y*side_len + side_len//2, dir)
            elif dir == 3:
                self.bullet = Bullet(self.x*side_len + side_len//2, self.y*side_len + side_len//2, dir)
            elif dir == 6:
                self.bullet = Bullet(self.x*side_len + side_len//2, self.y*side_len + side_len//2, dir)
            elif dir == 0:
                self.bullet = Bullet(self.x*side_len + side_len//2, self.y*side_len + side_len//2, dir)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)

    def change_color(self):
        self.color = -self.color

# everything about the enemy
class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect(center = (self.x * side_len + side_len//2, self.y * side_len + side_len//2))
    
    def draw(self):
        screen.blit(self.img, (self.x*side_len, self.y*side_len))

    def move(self):
        direction = random.randint(0,3)*3
        dx, dy = 0, 0
        if direction == 0:
            dy = 1
        elif direction == 3:
            dx = 1
        elif direction == 6:
            dy = -1
        elif direction == 9:
            dx = -1
        tx, ty = self.x+dx, self.y+dy
        if tx>=0 and tx<X and ty>=0 and ty<Y and grid[tx][ty].status == 1:
            collide = False
            for enemy in enemies:
                if tx == enemy.x and ty == enemy.y:
                    collide = True
                    break
            if not collide:
                self.x, self.y = tx, ty

        self.rect = self.img.get_rect(center = (self.x * side_len + side_len//2, self.y * side_len + side_len//2))

# everything about the soil_grid
class soil_grid(object):
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.status = status
    
    def draw(self):
        if self.status == 1:
            screen.blit(soil_img, (self.x*side_len, self.y*side_len))
        else:
            screen.blit(grass_img, (self.x*side_len, self.y*side_len))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):

        print(x, y, dir)

        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("bullet_1.png").convert_alpha(), (side_len, side_len))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED

        if dir == 0:
            self.x_vel, self.y_vel = 0, self.speed
        elif dir == 3:
            self.x_vel, self.y_vel = self.speed, 0
        elif dir == 6:
            self.x_vel, self.y_vel = 0, -self.speed
        else:
            self.x_vel, self.y_vel = -self.speed, 0

        # self.x_vel, self.y_vel = 0, 0

        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.center = (self.x, self.y)
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()

def draw_menu():
    bg = pygame.transform.scale(pygame.image.load("RADish_background.png").convert(), (X * side_len, Y * side_len))
    screen.blit(bg, (0,0))

# the function that draws everything in each round
def draw_gameplay():
    screen.fill((0,0,0))
    # draw soil
    for i in range(X):
        for j in range(Y):
            grid[i][j].draw()
    # draw raddish
    raddish.draw()
    # draw enemies
    for enemy in enemies:
        enemy.draw()

def draw_game_over():
    bg = ending_img
    screen.blit(bg, (0,0))

def draw_victory():
    bg = pygame.transform.scale(pygame.image.load("End_Screen.png").convert(), (X * side_len, Y * side_len))
    screen.blit(bg, (0,0))
# initialize

def check_ocupy(enemy_x, enemy_y):
    if enemy_x == raddish.x and enemy_y == raddish.y:
        return False
    for enemy in enemies:
        if enemy_x == enemy.x and enemy_y == enemy.y:
            return False
    return True

def game_initialize():
    global raddish, enemies, grid
    # create the initial position for raddish & enemies
    raddish = Raddish(x=random.randint(0,X-1), y=random.randint(0,Y-1), status=0)
    enemies = []
    for i in range(num_enemy):
        enemy_x, enemy_y = raddish.x, raddish.y
        while not check_ocupy(enemy_x, enemy_y):
            enemy_x, enemy_y = random.randint(0,X-1), random.randint(0,Y-1)
        enemies.append(enemy(x=enemy_x, y=enemy_y, img=enemy_img))

    # create the initial status for each soil grid

    grid=[]
    for i in range(X):
        row = []
        for j in range(Y):
            if not check_ocupy(i,j):
                row.append(soil_grid(x=i, y=j, status=1))
            else:
                if random.random() < soil_rate:
                    row.append(soil_grid(x=i, y=j, status=1))
                else:
                    row.append(soil_grid(x=i, y=j, status=-1))
        grid.append(row)

# flip_status: the action of a green raddish
def flip_status():
    dx, dy = 0, 0
    if raddish.status == 0:
            dy = 1
    elif raddish.status == 3:
            dx = 1
    elif raddish.status == 6:
            dy = -1
    elif raddish.status == 9:
            dx = -1
    
    tx, ty = raddish.x+dx, raddish.y+dy
    same_status = 0
    if tx>=0 and tx<X and ty>=0 and ty<Y:
        same_status = grid[tx][ty].status
    while tx>=0 and tx<X and ty>=0 and ty<Y and grid[tx][ty].status == same_status:
        if check_ocupy(tx, ty):
            grid[tx][ty].status=-grid[tx][ty].status
        tx += dx
        ty += dy

# start a new game
def new_game():
    pygame.mixer.music.unload()
    pygame.mixer.music.load('gameplay_music.mp3')
    pygame.mixer.music.play(loops=-1, start=0, fade_ms=2000)
    game_initialize()
    running = True
    mark = 1

    global bullet_group, all_sprites_group
    bullet_group = pygame.sprite.Group()
    all_sprites_group = pygame.sprite.Group()

    while running:
        mark = (mark+1) % enemy_moving_period
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # w,a,s,d : movement
                if event.key == pygame.K_s: # left
                    raddish.move(0)
                if event.key == pygame.K_d: # down
                    raddish.move(3)
                if event.key == pygame.K_w: # right
                    raddish.move(6)
                if event.key == pygame.K_a: # up
                    raddish.move(9)

                if event.key == pygame.K_SPACE: # shifting color
                    raddish.change_color()
                
                if raddish.shoot_cooldown > 0:
                    raddish.shoot_cooldown -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                # green raddish
                if raddish.color == 1:
                    xsf = pygame.mixer.Sound('build.mp3')
                    pygame.mixer.Sound.play(xsf)
                    flip_status()
                else:
                    raddish.shoot = True
                    raddish.is_shooting(raddish.status)
            else:
                raddish.shoot = False

        # random movement of enemy:
        if mark == 0:
            for enemy in enemies:
                if random.random() < enemy_movement_rate:
                    enemy.move()
        
        # Handle collision between bullet and enemy
        for bullet in bullet_group:
            if pygame.sprite.spritecollide(bullet, enemies, False):
                bullet.kill()
                to_delete = []
                for enemy in enemies:
                    if enemy.rect.colliderect(bullet.rect):
                        to_delete.append(enemy)
                for enemy in to_delete:
                    enemies.remove(enemy)
        
        # draw
        draw_gameplay()
        
        all_sprites_group.draw(screen)  
        all_sprites_group.update()

        
        # update the screen display
        pygame.display.flip()

        # check the collision between enemy & raddish
        for enemy in enemies:
            if enemy.x == raddish.x and enemy.y == raddish.y:
                game_over()
                return
        
        # check if win

        if len(enemies) == 0:
            mark = True
            for i in range(X):
                for j in range(Y):
                    if grid[i][j].status == -1:
                        mark = False
            if mark:
                victory()
                return

        # set limit on num of frames per second that game will render (cap the frame rate)
        clock.tick(100)

# after finishing a round
def game_over():
    pygame.mixer.music.unload()
    pygame.mixer.music.load('death_noise.wav')
    pygame.mixer.music.play(loops=0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                if mouse[0]>=804 and mouse[0]<1108 and mouse[1]>=528 and mouse[1]<=698:
                    new_game()
                    return

        draw_game_over()
        pygame.display.flip()

# victory
def victory():
    pygame.mixer.music.unload()
    pygame.mixer.music.load('victory_sound.mp3')
    pygame.mixer.music.play(loops=0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_victory()
        pygame.display.flip()

# starting page
def start_page():
    running = True
    pygame.mixer.music.load('title_music.mp3')
    pygame.mixer.music.play(loops=-1, start=0, fade_ms=2000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                if mouse[0]>=404 and mouse[0]<=819 and mouse[1]>=612 and mouse[1]<=727:
                    new_game()
                    return
        
        draw_menu()
        pygame.display.flip()


# main game loop
start_page()

# quit Pygame
pygame.quit()
sys.exit()