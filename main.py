import pygame

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAC-MAN")

FPS = 60                                    # frame per second


def draw_window():
    WIN.fill((255,255,255))                 # to change the background color
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