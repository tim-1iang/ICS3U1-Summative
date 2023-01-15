# gravity
# left and right wall collision
# ground collision
# player camera
# background image
# jump animation
# gravity ground animation to fix character going into ground


# Importing modules
import pgzrun

# Declaring the screen sizes
WIDTH = 1280
HEIGHT = 720
framesR = 0
framesL = 0
movement_y = 0
movement = 0

MAX_MOVEMENT = 6
MAX_GRAVITY = 9

# Declaration of variables and constants
current_level = "tutorial"

# Background
floor = Rect(0, 660, 3840, 720)
wall1 = Rect(500, 520, 520, 660)
wall2 = Rect(200, 520, 100, 660)
ground = [floor]
wall = [wall1]

# Entities
knight = Actor("idle/idle_r1")


# Function to draw into the game
def draw():
    screen.clear()
    screen.fill((200, 200, 200))
    knight.draw()
    screen.draw.filled_rect(floor, (106, 117, 141))
    screen.draw.filled_rect(wall1, (106, 117, 141))
    screen.draw.filled_rect(wall2, (106, 117, 141))

def character_gravity():
    pass

def character_collision():
    pass

def on_key_up(key):
    global framesL, framesR
    # Idle animation detection 
    if key == keys.LEFT:
        idle_animation()
    if key == keys.RIGHT:
        idle_animation()

def velocity():
    pass
'''
def jump():
    global movement_y
    pass


def on_key_down(key):
    if key == keys.X:
        jump()
'''

# Animation for running right
def running_right_animation():
    global framesR, direction
    framesR += 5
    if framesR >= 1 and framesR < 15:
        knight.image = "running/running_r1"
    elif framesR >= 20 and framesR < 30:
        knight.image = "running/running_r2"
    elif framesR >= 40 and framesR < 45:
        knight.image = "running/running_r3"
    elif framesR >= 60:
        framesR = 1
    direction = "right"

# Aniamtion for running left
def running_left_animation():
    global framesL, direction
    framesL += 5
    if framesL >= 1 and framesL < 15:
        knight.image = "running/running_l1"
    elif framesL >= 20 and framesL < 30:
        knight.image = "running/running_l2"
    elif framesL >= 40 and framesL < 45:
        knight.image = "running/running_l3"
    elif framesL >= 60:
        framesL = 1
    direction = "left"

def idle_animation():
    global direction
    if direction == "left":
        knight.image = "idle/idle_l1"
    elif direction == "right":
        knight.image = "idle/idle_r1"

# Function to update the game
def update():
    global framesL, framesR, direction, movement

    # Character Movement

    if keyboard.left:
        running_left_animation()
        '''
        for i in wall:
            if knight.colliderect(i) and direction == "left":
                continue
            elif i == wall[-1]:
                movement = -(MAX_MOVEMENT)
            else:
                movement = 0
        '''
        knight.x += movement

    if keyboard.right:
        running_right_animation()
        '''
        for i in wall:
            if knight.colliderect(i) and direction == "right":
                continue
            elif i == wall[-1]:
                movement = MAX_MOVEMENT
            else:
                movement = 0
        '''
        knight.x += movement

    if not(knight.colliderect(floor)):
        knight.y += 5

    # Collision



# Background Music

if current_level == "tutorial":
    music.play_once("tutorialmp")

pgzrun.go()
