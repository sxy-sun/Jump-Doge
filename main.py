import pygame
import os

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAC-MAN")

FPS = 60                                    # frame per second
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50        # size of the player, in case we want to resize later

# background image
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('assets','background.png')),(400, 400))    

PLAYER_IMAGE = pygame.image.load(os.path.join('assets','player.png'))      # Main player image
PLAYER = pygame.transform.scale(PLAYER_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT))    # scale


def draw_window(player):
    WIN.fill((0, 0, 0))
    WIN.blit(BACKGROUND,(180, 100))
    WIN.blit(PLAYER,(player.x, player.y))      # here we re-draw the thing with the pos of the rect
    
    pygame.display.update()

def player_movement(keys_pressed,player):          # the function to move the object
    if keys_pressed[pygame.K_LEFT]:
        player.x -= 50
    if keys_pressed[pygame.K_RIGHT]:
        player.x += 50
    if keys_pressed[pygame.K_DOWN]:
        player.y += 50
    if keys_pressed[pygame.K_UP]:
        player.y -= 50

def main():
    # create a rectangular to represent the player to control it
    player = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)       
    

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