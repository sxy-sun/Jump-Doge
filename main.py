import pygame
import os

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAC-MAN")

FPS = 60                                    # frame per second
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50        # size of the player, in case we want to resize later


BACKGROUND = pygame.image.load(os.path.join('assets','background.png'))     # background image
WEAK_DOGE_IMAGE = pygame.image.load(os.path.join('assets','weak.png'))      # Main player image
WEAK_DOGE = pygame.transform.scale(WEAK_DOGE_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT))    # scale


def draw_window():
    #WIN.fill((255,255,255))                 # to change the background color
    WIN.blit(WEAK_DOGE,(1,1))
    
    pygame.display.update()


def main():
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                         # control the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # when we want to quit the game
                run = False
    
        draw_window()
    
    pygame.quit()
    
    
    
if __name__ == "__main__":
    main()