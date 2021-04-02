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

WEAK_DOGE_IMAGE = pygame.image.load(os.path.join('assets','weak.png'))      # Main player image
WEAK_DOGE = pygame.transform.scale(WEAK_DOGE_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT))    # scale


def draw_window(weak):
    WIN.fill((0, 0, 0))
    WIN.blit(BACKGROUND,(180, 100))
    WIN.blit(WEAK_DOGE,(weak.x, weak.y))      # here we re-draw the thing with the pos of the rect
    
    pygame.display.update()

def weak_movement(keys_pressed,weak):          # the function to move the object
    if keys_pressed[pygame.K_LEFT]:
        weak.x -= 50
    if keys_pressed[pygame.K_RIGHT]:
        weak.x += 50
    if keys_pressed[pygame.K_DOWN]:
        weak.y += 50
    if keys_pressed[pygame.K_UP]:
        weak.y -= 50

def main():
    # create a rectangular to represent the weak_doge to control it
    weak = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)       
    

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                         # control the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # when we want to quit the game
                run = False
    
        keys_pressed = pygame.key.get_pressed() # detect which key is pressed
        weak_movement(keys_pressed, weak)       # pass the key to the move function
        draw_window(weak)                       # draw a new object aka the weak doge
    
    pygame.quit()
    
    
    
if __name__ == "__main__":
    main()