import pygame
import os

WIDTH, HEIGHT = 800, 600
FPS = 60                                    # frame per second
#PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50        # size of the player
#vel = 5                                     # velocity of the player

#isJump = False                              # is the doge in the jump motion
#jumpCount = 10

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUMP-DOGE")


class character(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        

player = character(0, HEIGHT - 50, 50, 50)

# background image
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('assets','background.png')),(400, 400))    

PLAYER_IMAGE = pygame.image.load(os.path.join('assets','player.png'))      # Main player image
PLAYER = pygame.transform.scale(PLAYER_IMAGE,(player.width,player.height))    # scale


def draw_window(player):
    WIN.fill((0, 0, 0))
    WIN.blit(BACKGROUND,(180, 100))
    WIN.blit(PLAYER,(player.x, player.y))      # here we re-draw the thing with the pos of the rect
    
    pygame.display.update()


def player_movement(keys_pressed, player):          # the function to move the object
    
    if keys_pressed[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
    if keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
        player.x += player.vel
    '''
    if keys_pressed[pygame.K_DOWN] and player.y < HEIGHT - PLAYER_HEIGHT - player.vel:
        player.y += player.vel
    '''
    
    # JUMP
    if not (player.isJump):
        if keys_pressed[pygame.K_UP]:
            player.isJump = True
    else:
        if player.jumpCount >= -10:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 10


def main():
    # create a rectangular to represent the player to control it
    # player = pygame.Rect(0, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)       
    

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                         # control the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # when we want to quit the game
                run = False
    
        keys_pressed = pygame.key.get_pressed() # detect which key is pressed
        player_movement(keys_pressed, player)       # pass the key to the move function
        draw_window(player)                       # draw a new object aka the player doge
    
    pygame.quit()
    
    
    
if __name__ == "__main__":
    main()