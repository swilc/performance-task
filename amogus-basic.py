# --> CONFIG <-- #
# Enable Debug Mode? 
DEBUG_MODE = True

# Delay between enemy spawning
ENEMY_DELAY = 1000

# Framerate the Game Uses
GAME_FPS = 60

# Font information (like the path to the font you want to use)
FONT = ".\\Simon_Wilch_Space_Invaders\\assets\\fonts\\vgasys.fon"
FONT_SIZE = 5
FONT_COLOR = (0, 255, 0)
# ------------------------------------------- #


PADDING = 100


# --> Variables that shouldn't be changed <-- #
# Path to Sprite Icons
PLAYER_ICON = ".\\amogus\\player.png"
PROJECTILE_ICON = ".\\Simon_Wilch_Space_Invaders\\assets\\images\\projectile.png"
ENEMY_ICON_DEFUALT = ".\\Simon_Wilch_Space_Invaders\\assets\\images\\enemy_default.png"
ENEMY_ICON1 = ".\\Simon_Wilch_Space_Invaders\\assets\\images\\enemy1.png"
ENEMY_ICON2 = ".\\Simon_Wilch_Space_Invaders\\assets\\images\\enemy2.png"

# Path to other images
BACKGROUND_IMAGE = ".\\amogus\\background.png"
SCOREBAR = ".\\Simon_Wilch_Space_Invaders\\assets\\images\\scorebar.png"
FINISHLINE = ".\\Simon_Wilch_Space_Invaders\\assets\\images\\finish.png"

# Path to highscore file
DATA_FILE = ".\\Simon_Wilch_Space_Invaders\\data\\highscore.json"

# Screen Resolution (You could technically change this but some assets won't work like intended)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# ------------------------------------------- #

# Import dependencies
import os
import json
import pygame
import random
from tkinter import *
from tkinter import messagebox
from pathlib import Path
from datetime import datetime

# Set the score and misses to 0
score = 0
misses = 0

# Hide the main Tktinker window on message box
Tk().wm_withdraw()

# Prints debug info to console with the message as the passed parameter
def debug(message):
    # Make sure debug mode is enabled.
    if DEBUG_MODE == True:
        # Send a debug message
        print("[DEBUG] >> " + str(message))

# Check if the game can access one of the files
# Convert this variable from str to Path
chk_file = Path(ENEMY_ICON_DEFUALT)
if chk_file.is_file() != True:
    # Send a debug message
    debug("Cannot access assets folder!")
    # If it couldn't access it, open a message box.
    messagebox.showinfo("Error", "Cannot access important assets. \nPlease check that the game's folder is in this directory:\n" + str(os.getcwd()))
else:
    debug("Looks like the assets folder is working.")

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# --> SETTING UP SPRITES <-- #
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load(PLAYER_ICON).convert_alpha()
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        )

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)

        # Keep player on the screen
        if self.rect.left < PADDING:
            self.rect.left = PADDING
            Background.update("left")
        if self.rect.right > SCREEN_WIDTH-PADDING:
            self.rect.right = SCREEN_WIDTH-PADDING
            Background.update("right")
        if self.rect.top < PADDING:
            self.rect.top = PADDING
            Background.update("up")
        if self.rect.bottom > SCREEN_HEIGHT-PADDING:
            self.rect.bottom = SCREEN_HEIGHT-PADDING
            Background.update("down")

bg_x = 0
bg_y = 0

# Set up the projectile sprite
class Background(pygame.sprite.Sprite):
    # This requires the X position of the player to be passed
    def __init__(self):
        super(Background, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.surf.set_colorkey((14, 207, 68))
        self.rect = self.surf.get_rect(
            center=((SCREEN_WIDTH,SCREEN_HEIGHT+500))
        )

    def plskill(self):
        self.kill()

    # Move the sprite based on user keypresses
    def update(direction):
        global bg_x
        global bg_y
        if direction == "right":
            bg_x -= 5
        if direction == "left":
            bg_x += 5
        if direction == "up":
            bg_y += 5
        if direction == "down":
            bg_y -= 5
        
    


# --> End of Defining Objects <-- #

# Define the addtext function which takes X and Y coords and a message and puts it on screen
def addtext(x, y, message):
    # Create a font object.
    font = pygame.font.Font(FONT, FONT_SIZE)
    # Create a text surface object to draw text on
    text = font.render(message, True, FONT_COLOR)
    # Create a rectangular object ("hitbox" of sorts) to draw the text on
    textRect = text.get_rect()
    # Set the center of the rectangular object.
    textRect.center = (x, y)
    # Put the text on the rectangle
    screen.blit(text, textRect)

# Load the high score from the data file
highscore = json.load(open(DATA_FILE))

# Set the pygame window name
pygame.display.set_caption('Space Invaders')

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Setup the game's clock speed
clock = pygame.time.Clock()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, ENEMY_DELAY)

# Instantiate player.
player = Player()
background = Background()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - finish is for the finish line to detect if an enemy got to the end
# - projectile is what gets launched
# - scorebar is the background for the score bar
# - all_sprites is used for rendering
thou_back = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Variable to keep the main loop running
running = True

# Send debug messages with info on the game settings
debug("Game Ready!")
debug("Resolution: " + str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT))
debug("Game Clock Speed/FPS: " + str(GAME_FPS))

# Add in the player sprite
all_sprites.add(player)
thou_back.add(background)
bg = pygame.image.load(BACKGROUND_IMAGE)
# Main loop
while running:
    #screen.blit(bg, (bg_x,bg_y))
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                # Send a debug message
                debug("Escape Key Pressed!")
                # End the loop
                running = False

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            # Send a debug message
            debug("Event Type \"Quit\" Called!")
            # End the loop
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    
    if pygame.sprite.collide_rect(player, background):
        # Send a debug message     
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        debug("Player on image at " + str(current_time))

    # Draw all sprites
    for entity in thou_back:
        screen.blit(entity.surf, (bg_x,bg_y))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()

    screen.fill((0,0,0))

    # Ensure program maintains a constant framerate (set in config)
    clock.tick(60)

# Send one last debug message signifying the end of the file
debug("EOF")

# Send a message to console which most people won't see
print("Thank you for playing!")
