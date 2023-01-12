# Importing modules
import pgzrun

# Declaring the screen size5
WIDTH = 1280
HEIGHT = 720

# Declaration of variables and constants
current_level = "tutorial"


# Entitiesm
knight = Actor("resting/tile000")
    

# Function to draw into the game
def draw():
    screen.clear()
    knight.draw()

    
# Function to update the game
def update():
    if keyboard.left:
        knight.x -= 5
    
    if keyboard.right:
        knight.x += 5
    

# Background Music 

if current_level == "tutorial":
    music.play_once("tutorialmp")

pgzrun.go() 
