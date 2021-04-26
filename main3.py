import pygame
import os
from pygame.locals import *

pygame.init()

width = 800
height = 600

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("JUMP-DOGE")

# define game variables
tile_size = 50


# Audio Load
pygame.mixer.init()    # something we have to do idk why
BULLETSOUND = pygame.mixer.Sound(os.path.join('assets', 'bullet.wav'))
BGM = pygame.mixer.music.load(os.path.join('assets', 'bgm.mp3'))

# Play the bgm continuously
# pygame.mixer.music.play(-1)

# load images
# sun_img = pygame.image.load('img/sun.png')
# bg_img = pygame.image.load('img/sky.png')
coin_group = pygame.sprite.Group()


def draw_grid():
    for line in range(0, 12):
        pygame.draw.line(WIN, (0, 0, 0), (0, line * tile_size),
                         (width, line * tile_size))

    for line in range(0, 16):
        pygame.draw.line(WIN, (0, 0, 0), (line * tile_size, 0),
                         (line * tile_size, height))


class character(object):
    def __init__(self, x, y, width, height):
        img = pygame.image.load((os.path.join('assets', 'playerL.png')))
        self.image = pygame.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.velY = 0
        self.isJump = False
        self.jumpCount = 8
        self.left = False
        self.right = True

    def draw(self, WIN):
        if self.left:
            WIN.blit(PLAYER_LEFT, (self.rect.x, self.rect.y))
        elif self.right:
            WIN.blit(PLAYER_RIGHT, (self.rect.x, self.rect.y))

    # decide the movement of the character
    def player_movement(self):
        keys_pressed = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys_pressed[pygame.K_LEFT] and self.rect.x > self.vel:
            dx -= self.vel
            self.left = True
            self.right = False
        elif keys_pressed[pygame.K_RIGHT] and self.rect.x < width - self.width - self.vel:
            dx += self.vel
            self.left = False
            self.right = True
        # JUMP
        if keys_pressed[pygame.K_UP] and self.isJump == False:
            self.isJump = True
            self.velY = -15

        if keys_pressed[pygame.K_UP] == False:
            self.isJump = False
            # self.velY = 0

        # gravity
        self.velY += 0.5
        if self.velY > 10:
            self.velY = 10
        dy += self.velY
        # if not (player.isJump):
        #     if keys_pressed[pygame.K_UP]:
        #         player.isJump = True
        # else:
        #     if player.jumpCount >= -8:
        #         neg = 1
        #         if player.jumpCount < 0:
        #             neg = -1
        #         player.y -= (player.jumpCount ** 2) * 0.5 * neg
        #         player.jumpCount -= 1
        #     else:
        #         player.isJump = False
        #         player.jumpCount = 8
        # check for collision
        for tile in world.tile_list:
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                # jumping
                if self.velY < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.velY = 0
                # falling
                elif self.velY >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.velY = 0
            # x direction
            # if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
            #     dx = 0
        # self.rect.x += dx
        # self.rect.y +=dy
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0
        if self.rect.top < 0:
            self.rect.top = 0
            dy = 0


# Here is the block for the floor
FLOOR_IMAGE = pygame.image.load(os.path.join('assets', 'dirt.png'))


class World():
    def __init__(self, data):
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(FLOOR_IMAGE, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    coin = Coin(col_count * tile_size + (tile_size//2),
                                row_count * tile_size + (tile_size//2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            WIN.blit(tile[0], tile[1])



world_data = [
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,2 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,1 ,1],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,2 ,2 ,2 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [1 ,1 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
]

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load((os.path.join('assets', 'coin.png')))
        self.image = pygame.transform.scale(img, (tile_size//2, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
     


def draw_window(player):
    WIN.fill((255, 255, 255))
    draw_grid() 
    player.draw(WIN)
    # enemy1.draw(WIN)
    # enemy2.draw(WIN)
    # for bullet in bullets:
        # bullet.draw(WIN)   
    world.draw()
    coin_group.draw(WIN)
    pygame.display.update()

player = character(0, height- 50, 50, 50)
world = World(world_data)


# Image Load
PLAYER_IMAGE_LEFT = pygame.image.load(os.path.join('assets','playerL.png'))      # player faces left
PLAYER_IMAGE_RIGHT = pygame.image.load(os.path.join('assets','playerR.png'))      # player faces right
PLAYER_LEFT = pygame.transform.scale(PLAYER_IMAGE_LEFT,(player.width,player.height))    # scale
PLAYER_RIGHT = pygame.transform.scale(PLAYER_IMAGE_RIGHT,(player.width,player.height))    # scale

# ENEMY_IMAGE = pygame.image.load(os.path.join('assets','enemy.png'))
# ENEMY = pygame.transform.scale(ENEMY_IMAGE,(enemy1.width,enemy1.height))

run = True
while run:

    # player.draw(WIN)
    # world.draw()
    # draw_grid()
    # player.player_movement(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # world.draw()
    # player.draw(WIN)
    
    player.player_movement()       # pass the key to the move function
    draw_window(player) 
    
    # pygame.display.update()
    

pygame.quit()
