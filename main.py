# things left to do
#####################
# left and right wall collision
# player camera
# shorten animation left and right code
# jump detect collision with max height
# differing jump heights depending on key hold
# attack cooldown


# Importing modules
import pgzrun
from pgzhelper import *

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
max_jump_height = 0
jump_time = 0
initial_height = 0
velocity_y = 0
touched_ground = False
stunned = False
attacked = False
attack_frame = 0
attack_time = 0
attack_cooldown = 0
cooldown_time = 0

MAX_MOVEMENT = 6
MAX_GRAVITY = 9.8
MAX_JUMP = 20
HEIGHT_LIMIT = 250
ATTACK_COOLDOWN_TIME = 20



# Background
background = Actor("background/tutorial_1", pos=(640, 360))
floor = Rect(0, 660, 3840, 720)
wall1 = Rect(500, 520, 520, 660)
wall2 = Rect(200, 520, 100, 660)
ground = [floor]
wall = [wall1]

# Entities
slash = Actor("attack/attack_slash_r", pos=(-50, -50))
knight = Actor("idle/idle_r1", anchor=("center", "bottom"), pos=(640, 0))


# Function to draw into the game
def draw():

    global attack_frame, attacked, current_level, attack_time
    screen.clear()

    background.draw()
    knight.draw()
    screen.draw.filled_rect(floor, (106, 117, 141))
    screen.draw.filled_rect(wall1, (106, 117, 141))
    screen.draw.filled_rect(wall2, (106, 117, 141))

    if attacked and attack_time >= 1:
        slash.draw()
        if current_level == "tutorial" and attack_time == 10:
            screen.clear()
            background.draw()
            knight.draw()
            screen.draw.filled_rect(floor, (106, 117, 141))
            screen.draw.filled_rect(wall1, (106, 117, 141))
            screen.draw.filled_rect(wall2, (106, 117, 141))
            


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
    global attacked, direction
    if direction == "left":
        slash.image = "attack/attack_slash_l"
        slash.pos = (knight.midleft[0] - 20, knight.midleft[1])
    elif direction == "right":
        temp_pos = knight.midright
        slash.image = "attack/attack_slash_r"
        slash.pos = (knight.midright[0] + 20, knight.midright[1])
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


        if key == keys.F:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, attack_cooldown)

        if key == keys.ESCAPE:
            exit()

        # Attack
        if key == keys.X and not(attack_cooldown):
            attack()


def jump_animation():
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    if jump_time >= 0 and jump_time < 5:
        knight.image = f"jumping/jumping_{temp}1"
    elif  jump_time >= 5 and jump_time < 20:
        knight.image = f"jumping/jumping_{temp}2"



def attack_animation():
    global attack_frame, direction, attacked
    attack_frame += 1

    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

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
    elif attack_frame >= 25:
        attack_frame = 0
        attacked = False


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
