'''
Emma McGrath
CIS_1051 Project

Catdash!
'''

import pygame
pygame.init()

#Window Title and Setup
pygame.display.set_caption('Catdash (trial)')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("lucidaconsole", 20)

#Images
background = pygame.image.load("C:\\Users\\emmam\\OneDrive\\Pictures\\Screenshots\\clouds.jpg").convert()
cat = pygame.image.load("C:\\Users\\emmam\\OneDrive\\Pictures\\Screenshots\\smallcat.png").convert_alpha()
spikes = pygame.image.load("C:\\Users\\emmam\\OneDrive\\Pictures\\Screenshots\\spikes.png").convert_alpha()
cloudscat1 = pygame.image.load("C:\\Users\\emmam\\OneDrive\\Pictures\\Screenshots\\ccd.jpg").convert()
cloudscat =  pygame.image.load("C:\\Users\emmam\\OneDrive\\Pictures\\Screenshots\\ccc.jpg").convert()

#Color
BLACK = (0, 0, 0)
PURPLE = (251, 160, 227)

#Global Variables
start = False
done = False
jumping = False
jump_count = 10

#Sprite Groups
all_sprites = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()

#Player sprite 
cat_rect = cat.get_rect(midbottom=(125, 550))
player_sprite = pygame.sprite.Sprite()
player_sprite.image = cat
player_sprite.rect = cat_rect
all_sprites.add(player_sprite)

#Spike class
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_spike = spikes
        scaled_width = 50  
        scaled_height = 40  
        self.image = pygame.transform.scale(original_spike, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self):
        self.rect.x -= 10  

#Start Screen
def start_screen():
    if not start:
        screen.blit(cloudscat1, (0, 0))
        welcome = font.render("Welcome to Catdash! Help this cat escape!", True, BLACK)
        controls = font.render("Press [SPACE] to play!", True, BLACK)
        screen.blits([[welcome, (100, 50)], [controls, (100, 425)]])

#Death Screen
def death():
    global fill
    fill = 0
    game_over = font.render("Game Over. You've upset him! Press  [SPACE] to restart", True, BLACK)
    screen.blit(cloudscat, (0, 0))
    screen.blits([[game_over, (100, 100)]])

    # Clearing out sprites
    spikes_group.empty()
    all_sprites.empty()

    # Reset cat position
    cat_rect.midbottom = (125, 550)
    player_sprite.rect = cat_rect


    key()

#Program waits for [SPACE]
def key():
    global level, start
    waiting = True
    while waiting:
        clock.tick(60)
        pygame.display.flip()

        if not start:
            start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Play Screen
def play():
    global jumping, jump_count
    screen.blit(background, (0, 0))
    #Purple floor
    rect_params = (0,550,800, 50)
    pygame.draw.rect(screen, PURPLE, rect_params)
    

    # Check for collisions with spikes
    spike_hit = pygame.sprite.spritecollide(player_sprite, spikes_group, False)
    if spike_hit:
        death()

    # Check for user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True

    # Update and draw spikes
    spikes_group.update()
    spikes_group.draw(screen)

    # Handle jumping
    if not jumping and keys[pygame.K_SPACE]:
        jumping = True

    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_sprite.rect.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    # Update cat_rect position
    cat_rect.midbottom = player_sprite.rect.midbottom

    # Check for collisions with the ground 
    ground_rect = pygame.Rect(0, screen.get_height() - 50, screen.get_width(), 50)
    if player_sprite.rect.colliderect(ground_rect):
        player_sprite.rect.y = ground_rect.top - player_sprite.rect.height
        jumping = False
        jump_count = 10

    # Check for collisions with spikes again after updating the position
    spike_hit = pygame.sprite.spritecollide(player_sprite, spikes_group, False)
    if spike_hit:
        death()

    # Draw the cat on the screen
    screen.blit(cat, cat_rect)
spike_speed = 10
#Last spike
last_spike_x = 900
distance_since_last_spike = 0
#Main Game Loop
while not done:
    if not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
        start_screen()
    else:
        play()
        

        # Check if the cat has collided with spikes
        spike_hit = pygame.sprite.spritecollide(player_sprite, spikes_group, False)
        if spike_hit:
            death()
            
        last_spike_x -= spike_speed
        distance_since_last_spike += 10  

        # Generate new spikes every 200 pixels
        if distance_since_last_spike >= 250 or not spikes_group:
            new_spike_x = max(last_spike_x + 200, screen.get_width())
            new_spike = Spike(new_spike_x, 550)
            spikes_group.add(new_spike)
            last_spike_x = new_spike_x
            distance_since_last_spike = 0
        # Update and draw sprites
        all_sprites.update()
        all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
