import pygame

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # when we want to quit the game
                run = False
    
    pygame.quit()
    
    
    
if __name__ == "__main__":
    main()