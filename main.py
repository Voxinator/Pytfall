import pygame
import sys

# Constants and settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 786
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
MAIN_MENU = 0
PLAYING = 1
GAME_OVER = 2

# Game timer
GAME_DURATION = 20 * 60 * 1000  # 20 minutes in milliseconds

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pitfall Clone")
clock = pygame.time.Clock()

# Fonts
menu_font = pygame.font.Font(None, 36)
timer_font = pygame.font.Font(None, 24)

# Game objects
# Define your game objects (player, obstacles, treasures) here

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_stand = pygame.image.load('player_image_stand.png').convert_alpha()
        self.image_jump = pygame.image.load('player_image_jump.png').convert_alpha()
        self.images_run = [
            pygame.image.load('player_image_run1.png').convert_alpha(),
            pygame.image.load('player_image_run2.png').convert_alpha(),
            pygame.image.load('player_image_run3.png').convert_alpha(),
            pygame.image.load('player_image_run4.png').convert_alpha()
        ]

        # Set initial image
        self.image = self.image_stand
        self.rect = self.image.get_rect()
      
        self.state = 'stand'
        self.animation_frame = 0
        self.direction = 'right'
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, SCREEN_HEIGHT - 100
        self.speed_x, self.speed_y = 0, 0
        self.is_jumping = False
        self.is_swinging = False


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -8
            if not self.is_jumping:
              self.state = 'run'
              self.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.speed_x = 8
            if not self.is_jumping:
              self.state = 'run'
              self.direction = 'right'
        else:
            self.speed_x = 0
            if not self.is_jumping:
              self.state = 'stand'
    def handle_jump_event(self, event):
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not self.is_jumping:
            self.speed_y = -15
            self.is_jumping = True
            self.state = 'jump'


        
        # elif event.type == pygame.KEYUP:
        #     if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
        #         self.speed_x = 0
        # if event.key in (pygame.K_UP, pygame.K_SPACE) and not self.is_jumping:
        #     self.speed_y = -15
        #     self.is_jumping = True
        #     for vine in vine_sprites:
        #         if pygame.sprite.collide_rect(self, vine):
        #             self.is_swinging = True
        #             break

    def update(self):
        self.rect.x += self.speed_x
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
      
        # Update player image based on the state
        if self.state == 'stand':
            self.image = self.image_stand
        elif self.state == 'jump':
            self.image = self.image_jump
        elif self.state == 'run':
            self.image = self.images_run[self.animation_frame // 3]  # Update the frame every 5 updates
            self.animation_frame = (self.animation_frame + 1) % 12   # Loop through the 4 running images
    
        # Flip the image if the player is facing left
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
      
        # Vertical movement and jumping
        self.rect.y += self.speed_y
        self.speed_y += 1  # Apply gravity
    
        ground_level = SCREEN_HEIGHT - 100  # Replace this with proper ground collision detection
        if self.rect.y >= ground_level:
            self.rect.y = ground_level
            self.is_jumping = False
            self.state = 'stand' if self.speed_x == 0 else 'run'
        else:
            self.state = 'jump'
          
        if self.is_swinging:
            # Apply swinging movement, e.g., move the player horizontally with the vine
            self.speed_x = 5
        else:
            self.speed_x = 0


# class Quicksand(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         # Load quicksand image, set initial position, etc.

#     def update(self):
#         # Update quicksand state, if necessary

# class RollingLog(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         # Load rolling log image, set initial position, etc.

#     def update(self):
#         # Update rolling log position and behavior

# class Vine(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         # Load vine image, set initial position, etc.



def draw_main_menu():
    start_game_text = menu_font.render("Start New Game", True, WHITE)
    start_game_rect = start_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_game_text, start_game_rect)

def handle_main_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return PLAYING
    return MAIN_MENU

def draw_timer(start_ticks):
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    remaining_ticks = GAME_DURATION - elapsed_ticks
    remaining_minutes = remaining_ticks // 60000
    remaining_seconds = (remaining_ticks % 60000) // 1000
    timer_text = timer_font.render(f"{remaining_minutes:02}:{remaining_seconds:02}", True, WHITE)
    screen.blit(timer_text, (10, 10))

# Game loop
game_state = MAIN_MENU
start_ticks = 0

# Create the player object and sprite group
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while True:
    if game_state == MAIN_MENU:
        game_state = handle_main_menu_events()
        draw_main_menu()
        start_ticks = pygame.time.get_ticks()  # Reset the start_ticks when returning to the main menu
    elif game_state == PLAYING:
        # Update game objects
        all_sprites.update()
        # obstacle_sprites.update
        # vine_sprites.update()
      
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            player.handle_jump_event(event)
            
        player.handle_input()
      
        # Collision detection
#        player_collisions = pygame.sprite.spritecollide(player, obstacle_sprites, False)
#        if player_collisions:
            # Handle collisions, e.g., reduce player health, end the game, etc.
#        player_vine_collisions = pygame.sprite.spritecollide(player, vine_sprites, False)
#        if player_vine_collisions:
            # Handle collisions, e.g., initiate swinging mechanics, end the swing based on player input, etc.
      
        # Update game objects
        # Call the update method for each game object

        # Create obstacle instances
        # quicksand1 = Quicksand(200, 400)
        # rolling_log1 = RollingLog(350, 300)
        # vine1 = Vine(500, 200)
        # ... add more instances as needed
        
        # Add obstacles to a sprite group
        # obstacle_sprites = pygame.sprite.Group()
        # obstacle_sprites.add(quicksand1, rolling_log1)  # Add more instances as needed
        # vine_sprites = pygame.sprite.Group()
        # vine_sprites.add(vine1)  # Add more instances as needed
      
        # Draw game objects
        screen.fill(BLACK)
        all_sprites.draw(screen)
        # obstacle_sprites.draw(screen)
        # vine_sprites.draw(screen)
        # Draw game objects on the screen here
        draw_timer(start_ticks)
    # else:
        # Other game states (e.g., GAME_OVER) can be handled here

    pygame.display.flip()
    clock.tick(FPS)