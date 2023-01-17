# left and right wall collision
# player camera
# background image
# jump and jump animation
# shorten animation left and right code
# jump detect collision with max height
# differing jump heights depending on key hold


# Importing modules
import pgzrun
from pgzhelper import *
from random import randint

# Declaring the screen sizes
WIDTH = 1280
HEIGHT = 720

# Declaration of variables and constants
current_level = "tutorial"
framesR = 0
framesL = 0
falling_time = 0
jumped = False
direction = "right"
bad_landing_time = 0
stunned_wait_time = 0
jumping_time = 0
max_jump_height = 0
jump_time = 0
initial_height = 0
velocity_y = 0
touched_ground = False
stunned = False
menu_choice = randint(0, 1)
attacked = False

MAX_MOVEMENT = 6
MAX_GRAVITY = 9.8
MAX_JUMP = 20
HEIGHT_LIMIT = 250



# Background
tutorial = ["background/tutorial_1", "background/tutorial_2"]
menu = ["background/menu_1", "background/menu_2"]
background = Actor(tutorial[0], pos=(640, 360))
floor = Rect(0, 660, 3840, 720)
wall1 = Rect(500, 520, 520, 660)
wall2 = Rect(200, 520, 100, 660)
ground = [floor]
wall = [wall1]


# Levels
levels = [menu, tutorial]


# Entities
knight = Actor("idle/idle_r1", anchor=("center", "bottom"), pos=(640, 0))


# Function to draw into the game
def draw():
    global direction
    screen.clear()
    
    '''
    # Menu
    if current_level == menu:
        background.draw()
    '''
    background.draw()
    knight.draw()
    screen.draw.filled_rect(floor, (106, 117, 141))
    screen.draw.filled_rect(wall1, (106, 117, 141))
    screen.draw.filled_rect(wall2, (106, 117, 141))
    
    if attacked:
        temp = ""
        if direction == "left":
            temp = "l" 
            temp_pos = knight.midleft
            temp_pos = (temp_pos[0] - 20, temp_pos[1])
        elif direction == "right":
            temp = "r"
            temp_pos = knight.midright
            temp_pos = (temp_pos[0] + 20, temp_pos[1])
        slash = Actor(f"attack/attack_slash_{temp}", pos=temp_pos)
        slash.draw()
    
    if current_level == "tutorial":
        pass
        


def character_gravity():
    global falling_time
    falling_time += 1
    if falling_time > 0 and falling_time <= 10:
        return MAX_GRAVITY * 0.3
    elif falling_time > 10 and falling_time <= 20:
        return MAX_GRAVITY * 0.6
    elif falling_time > 20 and falling_time <= 30:
        return MAX_GRAVITY * 0.9
    elif falling_time > 30:
        print(falling_time)
        return MAX_GRAVITY
    else:
        return 0


def on_key_up(key):
    global framesL, framesR, stunned
    # Idle animation detection
    if not (stunned):

        if key == keys.LEFT:
            idle_animation()
        if key == keys.RIGHT:
            idle_animation()


def jump():
    global MAX_JUMP, max_jump_height, jump_time, initial_height, jumped, HEIGHT_LIMIT, touched_ground
    jump_time += 1
    if jump_time == 1:
        touched_ground = False
        initial_height = knight.y
        max_jump_height = knight.y - HEIGHT_LIMIT

    if (
        knight.y <= initial_height and knight.y >= max_jump_height + (HEIGHT_LIMIT * 0.6)
    ):  # 75 50 25, 90 45 15
        velocity_y = MAX_JUMP
    elif initial_height - (HEIGHT_LIMIT * 0.6) <= knight.y and knight.y >= max_jump_height + (HEIGHT_LIMIT * 0.3):
        velocity_y = MAX_JUMP / 2
    elif initial_height - (HEIGHT_LIMIT * 0.9) <= knight.y and knight.y >= max_jump_height + (HEIGHT_LIMIT * 0.1):
        velocity_y = MAX_JUMP / 3
    elif knight.y >= max_jump_height:
        velocity_y = 0
        jump_time = 0
        jumped = False
    knight.y -= velocity_y

def attack():
    global attacked
    attacked = True

def on_key_down(key):
    global direction, jumped, stunned

    if not (stunned):

        if key == keys.LEFT:
            direction = "left"

        if key == keys.RIGHT:
            direction = "right"

        if key == keys.Z:
            if touched_ground:
                jumped = True
                jump()
                jump_animation()

        if key == keys.F:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

        if key == keys.ESCAPE:
            exit()

        # Attack
        if key == keys.X:
            attack()


def jump_animation():
    pass


# Animation for running right
def running_right_animation():
    global framesR
    framesR += 1
    if framesR >= 1 and framesR < 3:
        knight.image = "running/running_r1"
    elif framesR >= 3 and framesR < 6:
        knight.image = "running/running_r2"
    elif framesR >= 6 and framesR < 9:
        knight.image = "running/running_r3"
    elif framesR >= 12:
        framesR = 1


# Aniamtion for running left
def running_left_animation():
    global framesL
    framesL += 1
    if framesL >= 1 and framesL < 3:
        knight.image = "running/running_l1"
    elif framesL >= 3 and framesL < 6:
        knight.image = "running/running_l2"
    elif framesL >= 6 and framesL < 9:
        knight.image = "running/running_l3"
    elif framesL >= 12:
        framesL = 1


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
    global direction, MAX_MOVEMENT, falling_time, stunned, stunned_wait_time, jump_time, touched_ground

    if jump_time >= 1:
        jump()

    if stunned:
        if abs(time.time()) >= stunned_wait_time + 1:
            stunned = False

    # Character Movement
    if not (stunned):
        if keyboard.left:
            direction = "left"
            running_left_animation()
            knight.x -= MAX_MOVEMENT

        if keyboard.right:
            direction = "right"
            running_right_animation()
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
