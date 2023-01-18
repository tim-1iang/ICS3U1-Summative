# things left to do
#####################
# left and right wall collision
# player camera
# shorten animation left and right code
# jump detect collision with max height
# differing jump heights depending on key hold
# attack cooldown
# list for order of drawing in each level


# Importing modules
import pgzrun
from pgzhelper import *

# Declaring the screen sizes
WIDTH = 1280
HEIGHT = 720

# Declaration of variables and constants
current_level = "tutorial" # the current level the player is in
frames_running = 0 # the frames for the player running animation
falling_time = 0 # the time the player falls for
jumped = False # if the player jumped or not
direction = "right" # what direction the player is facing
bad_landing_time = 0 # counter for how long the landing animation is
stunned_wait_time = 0 # how long the player has to wait before they are not stunned
max_jump_height = 0 # the maxiumum height the player can jump depending on their current height
jump_time = 0 # how long the player will jump for
initial_height = 0 # the pos of the player
velocity_y = 0 # the vertical velocity the player will move in when jumping
touched_ground = False # if the player touched the ground or not
stunned = False # if the player is going to be stunned
attacked = False # if the player has attacked
attack_frame = 0 # the attack animation frames
attack_time = 0 # the time the player attacks for
attack_cooldown = False # if the player has attacked and will the next attack need a cooldown period
cooldown_time = 0 # the cooldown period counter for attacks

MAX_MOVEMENT = 6 # The maximum speed the player can move horizontally
MAX_GRAVITY = 9.8 # The maximum speed the player will fall at
MAX_JUMP = 20 # The maximum speed the player can jump at
HEIGHT_LIMIT = 250 # the height which the player cannot jump past
ATTACK_COOLDOWN_TIME = 20 # the time it takes before attacking again


# Background
background = Actor("background/tutorial_1", pos=(640, 360))
# Rects for the floors and walls
floor = Rect(0, 660, 3840, 720)
wall1 = Rect(500, 520, 520, 660)
wall2 = Rect(200, 520, 100, 660)


# Entities
slash = Actor("attack/attack_slash_r", pos=(-50, -50)) # the actor for the attack slash
knight = Actor("idle/idle_r1", anchor=("center", "bottom"), pos=(640, 0)) # the player actor


# Function to draw into the game
def draw():

    global attack_frame, attacked, current_level, attack_time # global variables
    screen.clear() # clear the screen

    background.draw() # draw the background actor
    knight.draw() # draw the player
    # draw the floor and wall rects
    screen.draw.filled_rect(floor, (106, 117, 141)) 
    screen.draw.filled_rect(wall1, (106, 117, 141))
    screen.draw.filled_rect(wall2, (106, 117, 141))

    if attacked and attack_time >= 1: # when the player attacked and the time they attacked for is greater or equal to 1
        slash.draw() # draw the attack slash
        if current_level == "tutorial" and attack_time == 10: # when the current_level is "tutorial" and the time they attacked for is 10
        # redraw the entire screen without the attack slash
            screen.clear()
            background.draw()
            knight.draw()
            screen.draw.filled_rect(floor, (106, 117, 141))
            screen.draw.filled_rect(wall1, (106, 117, 141))
            screen.draw.filled_rect(wall2, (106, 117, 141))


# function to calculate the player gravity speed
def character_gravity():
    global falling_time # global variables
    falling_time += 1 # increase falling_time everytime the function is ran
    # checks to see how long the player has been falling for
    # their falling speed will increase or decrease depending on how long it takes for the player to fall and touch the ground and is returned when the function is called
    if falling_time > 0 and falling_time <= 10:
        return MAX_GRAVITY * 0.3
    elif falling_time > 10 and falling_time <= 20:
        return MAX_GRAVITY * 0.6
    elif falling_time > 20 and falling_time <= 30:
        return MAX_GRAVITY * 0.9
    elif falling_time > 30:
        return MAX_GRAVITY
    else:
        return 0


# event handler function to check when the player lets go of a key, parameter key takes input of which key the user lifts up
def on_key_up(key):
    global stunned # global variables
    
    # Idle animation detection
    # checks if the player is stunned
    # then checks if the key they let go of is either left or right
    # if it is then the idle_animation function is called to change the animation state
    if not (stunned): 
        if key == keys.LEFT:
            idle_animation()
        if key == keys.RIGHT:
            idle_animation()


# Function for the player jumping
def jump():
    global MAX_JUMP, max_jump_height, jump_time, initial_height, jumped, HEIGHT_LIMIT, touched_ground # global variables
    jump_time += 1 # increase jump_time by one each time the function is called
    if jump_time == 1: # on the first call when jump_time is one
        touched_ground = False # the player is not touching the ground anymore
        initial_height = knight.y # the current height of the player is the initial height
        max_jump_height = knight.y - HEIGHT_LIMIT # the max height the player can jump is the value of height limit added above the player

    # checks if the player is between a certain height range based off the initial height and max jump height
    # depending on which height range they are in, the jump speed they will move at will change
    # the lower they are to where they started, the faster they are and vice versa
    if (knight.y <= initial_height and knight.y >= max_jump_height + (HEIGHT_LIMIT * 0.6)):
        velocity_y = MAX_JUMP
    elif initial_height - (HEIGHT_LIMIT * 0.6) <= knight.y and knight.y >= max_jump_height + (HEIGHT_LIMIT * 0.3):
        velocity_y = MAX_JUMP / 2
    elif initial_height - (HEIGHT_LIMIT * 0.9) <= knight.y and knight.y >= max_jump_height + (HEIGHT_LIMIT * 0.1):
        velocity_y = MAX_JUMP / 3
    elif knight.y >= max_jump_height: # when the player reaches the maximum height
        velocity_y = 0 # the jump velocity is set to 0
        jump_time = 0 # the time for the player to jump is resetted
        jumped = False # jumped is set to False so the player cannot jump until they touched the ground
        
    knight.y -= velocity_y # the player moves up depending on the jump speed everytime the function is called


# function for the player attacking
def attack():
    global attacked, direction # global variables
    
    if direction == "left": # if the player is facing left
        slash.image = "attack/attack_slash_l" # change the slash image to a left slash
        slash.pos = (knight.midleft[0] - 20, knight.midleft[1]) # the position of the attack slash is the same pos of the players midleft but to the left by 20 pixels
    elif direction == "right": # if the player is facing right
        slash.image = "attack/attack_slash_r" # change the slash image to a right slash
        slash.pos = (knight.midright[0] + 20, knight.midright[1]) # the position of the attack slash is the same pos of the players midright but to the right by 20 pixels
    attacked = True # set attacked to True meaning the player has attacked which will set off a cooldown


# event handler function for when a key is pressed down, parameter key is used to take input of which key the user pressed down
def on_key_down(key):
    global direction, jumped, stunned # global variables
    
    # checks individual keys
    if not (stunned): # if the player is not stunned, so the player cant move when they are stunned
        
        # left and right keys which changes the direction variable
        if key == keys.LEFT:
            direction = "left"

        if key == keys.RIGHT:
            direction = "right"

        # Z key for jumping
        if key == keys.Z:
            if touched_ground: # checks if the user has touched the ground before jumping
                jumped = True # change jumped to True meaning the user has jumped
                jump() # call the jump function

        # F key for putting the window in fullscreen
        if key == keys.F: 
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    
        # Escape key to exit the game
        if key == keys.ESCAPE:
            exit()

        # X key to attack only if attacking is not on cooldown
        if key == keys.X and not(attack_cooldown):
            attack()


# function for the jumping animation
def jump_animation():
    # temporary variable to change the animation more efficiently, helps with changing files depending on left or right
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"
    
    # animation will change depending on how long the player has jumped for
    # the player of the image is changed to animate it
    if jump_time >= 0 and jump_time < 5:
        knight.image = f"jumping/jumping_{temp}1"
    elif  jump_time >= 5 and jump_time < 20:
        knight.image = f"jumping/jumping_{temp}2"


# function for the attacking animation
def attack_animation():
    global attack_frame, direction, attacked # global variable
    attack_frame += 1 # adding one to attack_frame each time the attack animation function is called

    # temporary variable to change the animation more efficiently, helps with changing files depending on left or right
    temp = "" 
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    # animation will change depending on the frame of the attack_frame variable 
    # the image of the player actor will be changed to animate it
    if attack_frame >= 0 and attack_frame < 5:
        knight.image = f"attack/attack_{temp}1"
    elif attack_frame >= 5 and attack_frame < 10:
        knight.image = f"attack/attack_{temp}2"
    elif attack_frame >= 10 and attack_frame < 15:
        knight.image = f"attack/attack_{temp}3"
    elif attack_frame >= 15 and attack_frame < 20:
        knight.image = f"attack/attack_{temp}4"
    elif attack_frame >= 20 and attack_frame < 25:
        knight.image = f"attack/attack_{temp}5"
    # when the attack animation is done and the attack_frame is past the animation ranges
    elif attack_frame >= 25:
        attack_frame = 0 # the attack_frame counter is reset
        attacked = False # attacked is changed to False so the user can attack again


# function for the player running animation
def running_animation():
    global frames_running
    frames_running += 1
    
    # temporary variable to change the animation more efficiently, helps with changing files depending on left or right
    temp = "" 
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"
        
    if frames_running >= 1 and frames_running < 3:
        knight.image = f"running/running_{temp}1"
    elif frames_running >= 3 and frames_running < 6:
        knight.image = f"running/running_{temp}2"
    elif frames_running >= 6 and frames_running < 9:
        knight.image = f"running/running_{temp}3"
    elif frames_running >= 12:
        frames_running = 1

def idle_animation():
    global direction
    if direction == "left":
        knight.image = "idle/idle_l1"
    elif direction == "right":
        knight.image = "idle/idle_r1"


def fall_animation():
    global falling_time, direction
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    if falling_time > 0 and falling_time <= 10:
        knight.image = f"jumping/falling_{temp}1"
    elif falling_time > 10 and falling_time <= 20:
        knight.image = f"jumping/falling_{temp}2"
    elif falling_time > 20 and falling_time <= 30:
        knight.image = f"jumping/falling_{temp}3"


# bad landing = When the character hits the ground at a greater velocity, the character wont be able to move for a short duration
def landing_animation(bad_landing):
    global direction, bad_landing_time, stunned, stunned_wait_time
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    bad_landing_time += 1

    if bad_landing_time >= 1 and bad_landing_time <= 10:
        knight.image = f"jumping/landing_{temp}1"
        if bad_landing:
            stunned = True
            stunned_wait_time = abs(time.time())
    elif bad_landing:
        if bad_landing_time > 10 and bad_landing_time <= 20:
            knight.image = f"jumping/landing_{temp}2"
        elif bad_landing_time > 20 and bad_landing_time < 30:
            knight.image = f"jumping/landing_{temp}3"
    else:
        falling_time = 0


# Function to update the game
def update():
    global direction, falling_time, stunned, stunned_wait_time, jump_time, touched_ground, jumped, attacked, attack_time, attack_cooldown, cooldown_time
    global MAX_MOVEMENT, ATTACK_COOLDOWN_TIME

    if not(attacked) and not(jumped):
        idle_animation()

    if attack_cooldown:
        cooldown_time += 1
        if cooldown_time >= ATTACK_COOLDOWN_TIME:
            cooldown_time = 0
            attack_cooldown = False

    if attacked:
        attack_time += 1
        attack_animation()
        if attack_time >= 5:
            attack_time = 0
            attacked = False
            attack_cooldown = True

    if jump_time >= 1:
        jump()
        jump_animation()

    if stunned:
        if abs(time.time()) >= stunned_wait_time + 1:
            stunned = False

    # Character Movement
    if not (stunned):
        if keyboard.left:
            direction = "left"
            running_animation()
            knight.x -= MAX_MOVEMENT

        if keyboard.right:
            direction = "right"
            running_animation()
            knight.x += MAX_MOVEMENT

    # Collision
    # Gravity / Ground Collision
    if not (knight.colliderect(floor)) and not (jumped):
        knight.y += character_gravity()
        fall_animation()
    elif knight.colliderect(floor):
        touched_ground = True
        if falling_time > 0 and falling_time <= 30:
            landing_animation(False)
        elif falling_time > 30:
            landing_animation(True)
    else:
        falling_time = 0


# Background Music
if current_level == "tutorial":
    music.play_once("tutorialmp")

pgzrun.go()
