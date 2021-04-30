import pygame
import os
from pygame.locals import *
import random

pygame.init()

width = 800
height = 600

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dungeons and Doges")

# define game variables
tile_size = 50
gameover = 0  # 0 means current in the game, 1 means win, -1 means lose

# Audio Load
pygame.mixer.init()    # something we have to do idk why
BGM = pygame.mixer.music.load(os.path.join('assets', 'bgm.mp3'))

# Play the bgm continuously
pygame.mixer.music.play(-1)


coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
score = 0
# font
font = pygame.font.SysFont('Bauhaus 93', 35)
# color
black = (0, 0, 0)
blue = (0,0,255)


class character(object):
    def __init__(self, x, y, width, height):
        self.reset(x, y, width, height)

    def draw(self, WIN):
        if self.left:
            WIN.blit(PLAYER_LEFT, (self.rect.x, self.rect.y))
        elif self.right:
            WIN.blit(PLAYER_RIGHT, (self.rect.x, self.rect.y))
   
    def reset(self, x, y, width, height):
        img = pygame.image.load((os.path.join('assets', 'playerL.png')))
        self.image = pygame.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
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
        self.score = 0

    # decide the movement of the character
    def player_movement(self, gameover):
        keys_pressed = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if gameover == 0:
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
                self.velY = -12

            if keys_pressed[pygame.K_UP] == False:
                self.isJump = False
                # self.velY = 0

            # gravity
            self.velY += 0.5
            if self.velY > 10:
                self.velY = 10
            dy += self.velY

            # check collision with paltforms
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

            # check if get to the door
            if pygame.sprite.spritecollide(self, door_group, False):
                gameover = 1

            # check if lose
            if pygame.sprite.spritecollide(self, fire_group, False):
                gameover = -1
                
            # update locations
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.bottom > height:
                self.rect.bottom = height
                dy = 0
            if self.rect.top < 0:
                self.rect.top = 0
                dy = 0
        return gameover


player = character(0, height - 110, 50, 50)
# Image Load
PLAYER_IMAGE_LEFT = pygame.image.load(os.path.join(
    'assets', 'playerL.png'))      # player faces left
PLAYER_IMAGE_RIGHT = pygame.image.load(os.path.join(
    'assets', 'playerR.png'))      # player faces right 
PLAYER_LEFT = pygame.transform.scale(
    PLAYER_IMAGE_LEFT, (player.width, player.height))    # scale
PLAYER_RIGHT = pygame.transform.scale(
    PLAYER_IMAGE_RIGHT, (player.width, player.height))    # scale

FLOOR_IMAGE = pygame.image.load(os.path.join('assets', 'dirt.png'))

class World():
    def __init__(self, data):
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        FLOOR_IMAGE, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    coin = Coin(col_count * tile_size + (tile_size//2),
                                row_count * tile_size + (tile_size//2))
                    coin_group.add(coin)
                if tile == 3:
                    exit = Exit(col_count * tile_size + tile_size - (tile_size // 2),
                                row_count * tile_size + tile_size - (tile_size // 2))
                    door_group.add(exit)
                if tile == 4:
                    fire = FIRE(col_count * tile_size + tile_size - (tile_size // 2),
                                row_count * tile_size + tile_size - (tile_size // 2))
                    fire_group.add(fire)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            WIN.blit(tile[0], tile[1])


class Button():
    def __init__(self, x, y, img):
       self.image = img
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.clicked = False

    def draw(self):
        mouse = pygame.mouse.get_pos()
        isClicked = False
        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # if the left mouse is clicked
                self.clicked = True
                isClicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked == False
        WIN.blit(self.image, self.rect)
        return isClicked

# button 
RESTART = pygame.image.load(os.path.join(
                'assets', 'restart.png'))
restart = Button(width // 2 - 50, height // 2 + 50 , RESTART)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load((os.path.join('assets', 'exit.png')))
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load((os.path.join('assets', 'coin.png')))
        self.image = pygame.transform.scale(img, (tile_size//2, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class FIRE(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load((os.path.join('assets', 'fire.png')))
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


def create_world(i):
    if i == 1:
        world_data =  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [2, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]

    elif i == 2:
        world_data =  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]

    elif i == 3:
        world_data =  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]

    elif i == 4:
        world_data =  [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]


    return world_data

        
num = random.randint(1, 4)
world_data = create_world(num)
world = World(world_data)


def draw_message(text, font, color, x, y):
    img = font.render(text, True, color)
    WIN.blit(img, (x, y))


def reset_game():
    player.reset(0, height - 110, 50, 50)
    gameover = 0
    door_group.empty()
    coin_group.empty()
    fire_group.empty()
    num = random.randint(1, 5)
    world_data = create_world(num)
    world = World(world_data)
    return world


run = True
while run:
    WIN.fill((0,0,0))
    world.draw()
    player.draw(WIN)
    
    if gameover == 0:
        if pygame.sprite.spritecollide(player, coin_group, True):
            player.score += 1
        draw_message('Score: '+str(player.score), font, (255,255,255), tile_size - 10, 10)
    
    door_group.draw(WIN)
    coin_group.draw(WIN)
    fire_group.draw(WIN)

    gameover = player.player_movement(gameover)

    if gameover == 1:
        if player.score == 6:
            draw_message('YOU WIN!', font, blue, (width // 2) - 50, height // 2)
            if restart.draw():
                restart.clicked = False
                player.reset(0, height - 110, 50, 50)
                gameover = 0
                world = reset_game()
        elif player.score != 6:
            draw_message('PAY MORE', font, blue, (width // 2) - 55, height // 2)
            if restart.draw():
                restart.clicked = False
                player.reset(0, height - 110, 50, 50)
                gameover = 0
                world = reset_game()
    
    if gameover == -1:
        draw_message('YOU LOSE!', font, blue, (width // 2) - 50, height // 2)
        if restart.draw():
            restart.clicked = False
            player.reset(0, height - 110, 50, 50)
            gameover = 0
            world = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


pygame.quit()
