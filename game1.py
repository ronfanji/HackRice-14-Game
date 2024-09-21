import pygame
from sys import exit
import math

pygame.init()

WIDTH = 1500
HEIGHT = 800
FPS = 60
PLAYER_START_X = WIDTH//2
PLAYER_START_Y = HEIGHT//2
PLAYER_SIZE = 0.125
PLAYER_SPEED = 8
ENEMY_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RADish Beets 'em Up")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("hackathon/dirt.png").convert(), (WIDTH, HEIGHT))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("hackathon/radish_not_png.jpg").convert_alpha(), 0, PLAYER_SIZE) # change later
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        elif keys[pygame.K_s]:
            self.velocity_y = self.speed
        elif keys[pygame.K_d]:
            self.velocity_x = self.speed
        elif keys[pygame.K_a]:
            self.velocity_x = -self.speed
    
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load("hackathon/enemy_not_png.jpg").convert_alpha()
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

all_sprites_group.add(player)
all_sprites_group.add(enemy)

game_over = False

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not game_over:
        screen.blit(background, (0, 0))

        all_sprites_group.update()
        all_sprites_group.draw(screen)
        
        if pygame.sprite.collide_rect(player,enemy):
            game_over = True

    
    #screen.blit(player.image, player.pos)
    #player.update()

    pygame.display.update()
    clock.tick(FPS)