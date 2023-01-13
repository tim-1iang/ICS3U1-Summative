# Importing modules
import pgzrun

# Declaring the screen sizes
WIDTH = 1280
HEIGHT = 720
framesR = 0

# Declaration of variables and constants
current_level = "tutorial"

# Background
floor = Rect(0, 660, 3840, 720)
environment = [floor]

# Entities
knight = Actor("resting/resting_r1")


# Function to draw into the game
def draw():
    screen.clear()
    knight.draw()
    screen.draw.filled_rect(floor, (106, 117, 141))

def character_gravity():
    pass
    
def character_collision():
    pass

def on_key_up():
    pass

def walkRightAnimation():
    global framesR
    framesR += 1
    if framesR == 1:
        knight.image = "running/running_r1"
    elif framesR== 20:
        knight.image = "running/running_r2"
    elif framesR == 40:
        knight.image = "running/running_r3"
    elif framesR >= 60:
        framesR= 1
    framesR = 0
    
    
def walkLeftAnimation():
    frames = 0
    frames += 1
    
    

# Function to update the game
def update():
    
    # Character Movement
    if keyboard.left:
        walkLeftAnimation()
        knight.x -= 5

    if keyboard.right:
        walkRightAnimation()
        knight.x += 5
    
    if keyboard[keys.X]:
        knight.y -= 10
        
    if not(knight.colliderect(floor)):
        knight.y += 5
    # Collision 
    


# Background Music

if current_level == "tutorial":
    music.play_once("tutorialmp")

pgzrun.go() 
