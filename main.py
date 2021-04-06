import pygame
import os

WIDTH, HEIGHT = 800, 600
FPS = 60     # frame per second

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
        self.left = False
        self.right = True
        

player = character(0, HEIGHT - 50, 50, 50)

# Image Load
PLAYER_IMAGE_LEFT = pygame.image.load(os.path.join('assets','playerL.png'))      # player faces left
PLAYER_IMAGE_RIGHT = pygame.image.load(os.path.join('assets','playerR.png'))      # player faces right
PLAYER_LEFT = pygame.transform.scale(PLAYER_IMAGE_LEFT,(player.width,player.height))    # scale
PLAYER_RIGHT = pygame.transform.scale(PLAYER_IMAGE_RIGHT,(player.width,player.height))    # scale

# Audio Load
pygame.mixer.init()    # something we have to do idk why
BULLETSOUND = pygame.mixer.Sound(os.path.join('assets','bullet.wav'))    
BGM = pygame.mixer.music.load(os.path.join('assets','bgm.mp3'))    

# Play the bgm continuously 
pygame.mixer.music.play(-1) 


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, WIN):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)


def draw_window(player):
    WIN.fill((0, 0, 0))
    player.draw(WIN)
    for bullet in bullets:
        bullet.draw(WIN)
        
    pygame.display.update()
    
    
def player_movement(keys_pressed, player):      
    if keys_pressed[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
    elif keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - player.width - player.vel:
        player.x += player.vel
        player.left = False
        player.right = True

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
            
    # SHOOTING
    global shootLoop
    if keys_pressed[pygame.K_SPACE] and shootLoop == 0:
        if player.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:               # allow only 5 bullets existing on the screen at once
            bullets.append(projectile(round(player.x + player.width //2), 
                                      round(player.y + player.height //2),
                                      6, (255, 255, 0), facing))
            BULLETSOUND.play()
        shootLoop = 1

bullets = []    # where we contain all the bullets
shootLoop = 0
def main():
    global shootLoop
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)                         # control the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # when we want to quit the game
                run = False
                
        if shootLoop > 0:   shootLoop += 1
        if shootLoop > 3:   shootLoop = 0
        
        for bullet in bullets:
            if bullet.x < WIDTH and bullet.x > 0:
                bullet.x += bullet.vel  # Moves the bullet by its vel
            else:
                bullets.pop(bullets.index(bullet))  # remove the bullet if it is off the screen
        
        keys_pressed = pygame.key.get_pressed()     # detect which key is pressed
        player_movement(keys_pressed, player)       # pass the key to the move function
        draw_window(player)                         # draw a new object aka the player doge
    
    pygame.quit()
    
    
if __name__ == "__main__":
    main()