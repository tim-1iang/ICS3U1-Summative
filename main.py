
# Importing modules
import pgzrun
from pgzhelper import *
from random import randint

# Declaring the screen sizes
WIDTH = 1280
HEIGHT = 720

# Declaration of variables and constants
current_level = "birth" # the current level the player is in
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
attack_cooldown = False # if the player has attacked and will the next attack need a cooldown period
cooldown_time = 0 # the cooldown period counter for attacks
level_changed = False
left_border = 15
right_border = 1265
chat_lock = False
gruz_mother_frames = 0
gruz_awake = False
gruz_mother_phase = "sleeping"
hit_cooldown = False
hit_cooldown_time = 0
hornet_animation_frames = 0
next_line = False
current_line = -1
interacted_with = ""
gruz_direction = "l"
gruz_x = -4
gruz_y = -3
gruz_animation_loops = 0
gruz_one_hit = False
gruz_to_knight_direction = "l"
gruz_charged = False
music_changed = True


MAX_MOVEMENT = 8 # The maximum speed the player can move horizontally
MAX_GRAVITY = 9.8 # The maximum speed the player will fall at
MAX_JUMP = 20 # The maximum speed the player can jump at
HEIGHT_LIMIT = 250 # the height which the player cannot jump past
ATTACK_COOLDOWN_TIME = 20 # the time it takes before attacking again
HEALTH_LIMIT = 5
MAX_FOCUS = 5
HIT_COOLDOWN_TIME = 100
TEXT_BOX_POS = (640, 120)
GRUZ_MOTHER_MAX_HEALTH = 10


health_left = HEALTH_LIMIT
gruz_health = GRUZ_MOTHER_MAX_HEALTH

# Entities
hornet = Actor("hornet/idle/hornet_idle_r", pos=(-50, -50), anchor=("center", "bottom"))
slash = Actor("attack/attack_slash_r", pos=(-1000, -1000)) # the actor for the attack slash
knight = Actor("idle/idle_r1", anchor=("center", "bottom"), pos=(640, 0)) # the player actor, the player anchor is like the point which moves when the player is moved
gruz_mother = Actor("gruzmother/sleeping/1", pos=(-200, -200), anchor=("center", "bottom"))
enemies = [gruz_mother]

# Background
focus_bar = Actor("inventory/focus_bar1", pos=(30, 30), anchor=("left", "top"))
health_bar = []

for i in range(0, HEALTH_LIMIT):
    health = Actor("inventory/health", pos=(125 + (i * 45), 85), anchor=("left", "top"))
    health_bar.append(health)

tutorial_door = Actor("background/door", pos=(-50, -50), anchor=("middle", "bottom"))
birth_bg = Actor("background/birth/mainbg", pos=(640, 360))
floor = Actor("background/floor", pos=(-200, -200), anchor=("left", "bottom"))
floor2 = Actor("background/floor", pos=(-200, -200), anchor=("left", "bottom"))
tutorial_bg = Actor("background/tutorial/mainbg", pos=(640, 360))
scene1_bg1 = Actor("background/scene1/mainbg", pos=(0, 0), anchor=("left", "top"))
scene1_bg2 = Actor("background/scene1/bg_2", pos=(1200, 0), anchor=("left", "top"))
bossfight_bg = Actor("background/bossfight/mainbg", anchor=("left", "top"), pos=(0, 0))
tutorial_overlay1 = Actor("background/tutorial/overlay1", pos=(0, 740), anchor=("left", "bottom"))
scene1_door = Actor("background/door", pos=(-50, -50), anchor=("middle", "bottom"))
bossfight_door = Actor("background/door", pos=(-50, -50), anchor=("middle", "bottom"))
textbox = Actor("textboxes/textbox", pos=(-100, -100), anchor=("middle", "middle"))

# Dialouge/gametips
interact_key = Actor("keys/fkey", anchor=("center", "bottom"), pos=(-50, -50))
enter_key = Actor("keys/enterkey", anchor=("center", "bottom"), pos=(-50, -50))
dialouge = ["HOW DARE YOU BREAK IN TO HALLOWNEST!",
            "You don't remember anything?",
            "Sorry for being rude, theres been a lot of problems recently.\nMy name is Hornet and I'm the guardian of Hallownest."
            "This is a dangerous place to be in.\nHallownest has fallen into ruin ever since the infection started.",
            "As long as you pass my trial, I'll let you pass through.",
            "There's a large creature that I want you to kill.",
            "You can find it in the shrine towards the east side of the village.",
            ]

# Rects for the floors and walls
#floor = Rect(0, 660, 3840, 720)
wall1 = Rect(500, 520, 520, 660)
wall2 = Rect(100, 520, 120, 660)

birth = [birth_bg, slash, knight, focus_bar]
tutorial = [tutorial_bg, floor, tutorial_door, hornet, slash, knight, focus_bar, interact_key]
scene1 = [scene1_bg1, scene1_bg2, scene1_door, bossfight_door, floor, floor2, slash, knight, focus_bar, interact_key]
bossfight = [bossfight_bg, floor, focus_bar, interact_key, gruz_mother, slash, knight]

# Function to draw into the game
def draw():
    global attack_frame, attacked, current_level # global variables

    level_draw()

    if chat_lock:
        if interacted_with == "hornet":
            hornet_dialouge()


def level_draw():
    screen.clear()

    if current_level == "birth":
        for x in birth:
            x.draw()
    elif current_level == "tutorial":
        for x in tutorial:
            x.draw()
    elif current_level == "scene1":
        for x in scene1:
            x.draw()
    elif current_level == "bossfight":
        for x in bossfight:
            x.draw()

    for y, z in enumerate(health_bar):
        z.draw()
    textbox.draw()
    enter_key.draw()

def hornet_dialouge():
    global next_line, current_line, chat_lock, textbox, enter_key
    if not(current_line == len(dialouge)):
        screen.draw.text(dialouge[current_line], center=TEXT_BOX_POS)
        if not(next_line):
            next_line = True
            current_line += 1
    else:
        current_line = -1
        chat_lock = False
        textbox.pos = (-100, -100)
        enter_key.pos = (-100, -100)



def game_over():
    print ("dead")

def hit(enemy):
    global health_bar, health_left, hit_cooldown
    health_left -= 1
    health_bar[health_left].image = "inventory/empty"
    if health_left == 0:
        game_over()
    hit_cooldown = True


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
    global direction, jumped, stunned, current_level, level_changed, textbox, chat_lock, next_line, interacted_with, enter_key # global variables

    if next_line:
        if key == keys.RETURN:
            next_line = False

    if key == keys.U:
        print (knight.pos, "knight.pos")
        print (touched_ground, "touched_ground")
        print (jumped, "jumped")
        print (attacked, "attacked")
        print (current_level, "current_level")
        print (gruz_mother_phase, "gruz_mother_phase")
        print (gruz_health, "gruz_health")
        print (gruz_animation_loops, "gruz_animation_loops")
        print (gruz_x, "gruz_x", gruz_y, "gruz_y")
        print (gruz_mother.pos, "gruz_pos")
        print (gruz_direction, "gruz_direction")

    if key == keys.L:
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # Escape key to exit the game
    if key == keys.ESCAPE:
        exit()

    # checks individual keys
    if not (stunned) and not(chat_lock): # if the player is not stunned, so the player cant move when they are stunned

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
            if knight.colliderect(tutorial_door):
                level_changed = True
                current_level = "scene1"
            elif knight.colliderect(hornet):
                interacted_with = "hornet"
                textbox.pos = TEXT_BOX_POS
                enter_key.pos = (970, 200)
                chat_lock = True
            elif knight.colliderect(scene1_door):
                level_changed = True
                current_level = "tutorial"
            elif knight.colliderect(bossfight_door):
                level_changed = True
                current_level = "bossfight"

        # X key to attack only if attacking is not on cooldown
        if key == keys.X and not(attack_cooldown):
            attack()

# function for the jumping animation
def jump_animation():
    # temporary variable to change the animation more efficiently, helps with changing image files depending on left or right
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

    # temporary variable to change the animation more efficiently, helps with changing image files depending on left or right
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

    # temporary variable to change the animation more efficiently, helps with changing image files depending on left or right
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    # checks which frame frames_running is at and depending on the frame will change the image of the player
    if frames_running >= 1 and frames_running < 3:
        knight.image = f"running/running_{temp}1"
    elif frames_running >= 3 and frames_running < 6:
        knight.image = f"running/running_{temp}2"
    elif frames_running >= 6 and frames_running < 9:
        knight.image = f"running/running_{temp}3"
    # once all the running images are animated, frames_running is reset to 1 so the images will loop
    elif frames_running >= 12:
        frames_running = 1


# function for the players idle animation
def idle_animation():
    global direction # global variable
    # depending on which direction is player is facing, the idle animation will either be left or right through changing the players actor image
    if direction == "left":
        knight.image = "idle/idle_l1"
    elif direction == "right":
        knight.image = "idle/idle_r1"


# function for the players fall animation
def fall_animation():
    global falling_time, direction # global variables

    # temporary variable to change the animation more efficiently, helps with changing image files depending on left or right
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    # depending on how long the player has been falling for the players actor image will change
    if falling_time > 0 and falling_time <= 10:
        knight.image = f"jumping/falling_{temp}1"
    elif falling_time > 10 and falling_time <= 20:
        knight.image = f"jumping/falling_{temp}2"
    elif falling_time > 20 and falling_time <= 30:
        knight.image = f"jumping/falling_{temp}3"


# function for the players landing animation after falling
# bad landing = When the character hits the ground at a greater velocity, the character wont be able to move for a short duration
# this function takes in the parameter bad_landing which tells you if the user will be having a bad landing, is a boolean
def landing_animation(bad_landing):
    global direction, bad_landing_time, stunned, stunned_wait_time, falling_time # global variables

    # temporary variable to change the animation more efficiently, helps with changing image files depending on left or right
    temp = ""
    if direction == "left":
        temp = "l"
    elif direction == "right":
        temp = "r"

    bad_landing_time += 1 # add one to the bad landing counter each time the function is called

    # the player actor's images will change depending on the bad landing frame counter range
    if bad_landing_time >= 1 and bad_landing_time <= 10:
        knight.image = f"jumping/landing_{temp}1"
        if bad_landing: # if the player has a bad landing
            stunned = True # stunned is set to True so the player will be stunned
            stunned_wait_time = abs(time.time()) # the time of the stun
    # if the player does not have a bad landing the next landing animation will not run
    elif bad_landing:
        if bad_landing_time > 10 and bad_landing_time <= 20:
            knight.image = f"jumping/landing_{temp}2"
        elif bad_landing_time > 20 and bad_landing_time < 30:
            knight.image = f"jumping/landing_{temp}3"

def gruz_mother_animation():
    global gruz_mother_frames, gruz_mother, gruz_mother_phase, gruz_direction, gruz_animation_loops, gruz_health, gruz_to_knight_direction, gruz_direction
    if knight.x <= gruz_mother.x:
        gruz_to_knight_direction = "l"
    elif knight.x > gruz_mother.x:
        gruz_to_knight_direction = "r"

    gruz_mother_frames += 1
    if gruz_mother_phase == "sleeping":
        if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = "gruzmother/sleeping/1"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = "gruzmother/sleeping/2"
        elif gruz_mother_frames > 20 and gruz_mother_frames <= 30:
            gruz_mother.image = "gruzmother/sleeping/3"
        elif gruz_mother_frames > 30 and gruz_mother_frames <= 40:
            gruz_mother.image = "gruzmother/sleeping/4"
        elif gruz_mother_frames > 40 and gruz_mother_frames <= 50:
            gruz_mother.image = "gruzmother/sleeping/5"
        elif gruz_mother_frames > 50 and gruz_mother_frames <= 60:
            gruz_mother.image = "gruzmother/sleeping/6"
        elif gruz_mother_frames > 60 and gruz_mother_frames <= 70:
            gruz_mother.image = "gruzmother/sleeping/7"
        elif gruz_mother_frames > 70 and gruz_mother_frames <= 80:
            gruz_mother.image = "gruzmother/sleeping/8"
        elif gruz_mother_frames > 80:
            gruz_mother_frames = 1
    elif gruz_mother_phase == "wakeup" or gruz_mother_phase == "dying":
        if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = "gruzmother/wakeup/1"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = "gruzmother/wakeup/2"
        elif gruz_mother_frames > 20 and gruz_mother_frames <= 30:
            gruz_mother.image = "gruzmother/wakeup/3"
        elif gruz_mother_frames > 30 and gruz_mother_frames <= 40:
            gruz_mother.image = "gruzmother/wakeup/4"
        elif gruz_mother_frames > 40 and gruz_mother_phase == "wakeup":
            if gruz_animation_loops >= 1:
                gruz_mother_phase = "flying"
                gruz_animation_loops = 0
            else:
                gruz_animation_loops += 1
            gruz_mother_frames = 1
        elif gruz_mother_frames > 40 and gruz_mother_phase == "dying":
            if gruz_animation_loops >= 3:
                gruz_mother_phase = "fall"
                gruz_animation_loops = 0
                gruz_health = -1
            else:
                gruz_animation_loops += 1
            gruz_mother_frames = 1
    elif gruz_mother_phase == "flying":
        if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = f"gruzmother/flying/1{gruz_direction}"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = f"gruzmother/flying/2{gruz_direction}"
        elif gruz_mother_frames > 20 and gruz_mother_frames <= 30:
            gruz_mother.image = f"gruzmother/flying/3{gruz_direction}"
        elif gruz_mother_frames > 30 and gruz_mother_frames <= 40:
            gruz_mother.image = f"gruzmother/flying/4{gruz_direction}"
        elif gruz_mother_frames > 40:
            gruz_mother_frames = 1
            gruz_animation_loops += 1
    elif gruz_mother_phase == "fall":
        if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = f"gruzmother/dead/1"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = f"gruzmother/dead/2"
        elif gruz_mother.colliderect(floor):
            gruz_mother_frames = 1
            gruz_mother_phase = "wiggle"
    elif gruz_mother_phase == "wiggle":
        if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = f"gruzmother/dead/wiggle/1"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = f"gruzmother/dead/wiggle/2"
        elif gruz_mother_frames > 20 and gruz_mother_frames <= 30:
            gruz_mother.image = f"gruzmother/dead/wiggle/3"
        elif gruz_mother_frames > 30:
            gruz_mother_phase = "stop"
            gruz_mother_frames = 1
    elif gruz_mother_phase == "stop":
        if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = f"gruzmother/dead/stop/1"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = f"gruzmother/dead/stop/2"
        elif gruz_mother_frames > 20 and gruz_mother_frames <= 30:
            gruz_mother.image = f"gruzmother/dead/stop/3"
    elif gruz_mother_phase == "charge":
        if gruz_animation_loops == 1:
            if gruz_mother_frames > 0 and gruz_mother_frames <= 10:
                gruz_mother.image = f"gruzmother/charge/6{gruz_to_knight_direction}"
            elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
                gruz_mother.image = f"gruzmother/charge/7{gruz_to_knight_direction}"
            elif gruz_mother_frames > 20:
                gruz_animation_loops = 0
                gruz_mother_phase = "flying"
                gruz_mother_frames = 1
        elif gruz_mother_frames > 0 and gruz_mother_frames <= 10:
            gruz_mother.image = f"gruzmother/charge/1{gruz_to_knight_direction}"
        elif gruz_mother_frames > 10 and gruz_mother_frames <= 20:
            gruz_mother.image = f"gruzmother/charge/2{gruz_to_knight_direction}"
        elif gruz_mother_frames > 20 and gruz_mother_frames <= 30:
            gruz_mother.image = f"gruzmother/charge/3{gruz_to_knight_direction}"
        elif gruz_mother_frames > 30 and gruz_mother_frames <= 40:
            gruz_mother.image = f"gruzmother/charge/4{gruz_to_knight_direction}"
        elif gruz_mother_frames > 40 and gruz_mother_frames <= 50:
            gruz_mother.image = f"gruzmother/charge/5{gruz_to_knight_direction}"
        elif gruz_mother.midleft[0] <= 0 or gruz_mother.midright[0] >= 1280 or gruz_mother.midtop[1] <= 0 or gruz_mother.colliderect(floor):
            gruz_animation_loops += 1
            gruz_mother_frames = 1
    elif gruz_mother_phase == "slam":
        # every slam is one animation loop, check gruz_mother's closest ceiling/floor
        if gruz_animation_loops % 2 == 0:

            if gruz_mother.midtop[1] <= 50 and gruz_mother.midtop[1] >= 0:
                gruz_mother.image = f"gruzmother/slam/up_{gruz_direction}"
            else:
                gruz_mother.image = f"gruzmother/slam/recover_{gruz_direction}"

        elif gruz_animation_loops % 2 == 1:

            if gruz_mother.midbottom[1] >= floor.midtop[1] - 50 and gruz_mother.midbottom[1] <= floor.midtop[1]:
                gruz_mother.image = f"gruzmother/slam/down_{gruz_direction}"
            else:
                gruz_mother.image = f"gruzmother/slam/recover_{gruz_direction}"

        if gruz_mother.midtop[1] <= 0 or gruz_mother.midbottom[1] >= floor.midtop[1]:
            gruz_animation_loops += 1

        if gruz_animation_loops == 12:
            gruz_mother_frames = 0
            gruz_animation_loops = 0
            gruz_mother_phase = "flying"



def gruz_mother_fight():
    global gruz_mother_phase, gruz_direction, gruz_health, gruz_x, gruz_y, gruz_one_hit, enemies, gruz_animation_loops, gruz_to_knight_direction, gruz_charged

    if gruz_mother_phase == "slam":
        if gruz_mother.midright[0] >= 1280 or gruz_mother.midleft[0] <= 0:
            if gruz_direction == "l":
                gruz_direction = "r"
            else:
                gruz_direction = "l"
        if gruz_animation_loops % 2 == 0:
            gruz_y = 15
        elif gruz_animation_loops % 2 == 1:
            gruz_y = -15

        if gruz_direction == "l":
            gruz_x = -7
        elif gruz_direction == "r":
            gruz_x = 7

    if gruz_mother_phase == "fall" and not(gruz_mother.colliderect(floor)):
        gruz_mother.y += MAX_GRAVITY

    if slash.colliderect(gruz_mother) and gruz_health != -1 and not(gruz_one_hit):
        gruz_one_hit = True
        gruz_health -= 1
    elif not(slash.colliderect(gruz_mother)):
        gruz_one_hit = False

    if gruz_health == 0 and gruz_mother in enemies:
        gruz_mother_phase = "dying"
        enemies.remove(gruz_mother)

    if gruz_mother_phase == "flying" and gruz_animation_loops >= 10:
        num = randint(1, 3)
        gruz_animation_loops = 0
        if num == 1:
            gruz_mother_phase = "charge"
            gruz_x = 0
            gruz_y = 0
        elif num > 1:
            gruz_mother_phase = "slam"
            gruz_x = 0
            gruz_y = 0

    if gruz_mother_phase == "flying":
        if gruz_mother.midright[0] >= 1280:
            gruz_direction = "l"
            gruz_x = -4

        elif gruz_mother.midleft[0] <= 0:
            gruz_direction = "r"
            gruz_x = 4

        if gruz_mother.midtop[1] <= 0:
            gruz_y = 3
        elif gruz_mother.midbottom[1] >= floor.midtop[1]:
            gruz_y = -3

    # x is fixed movespeed while y can vary
    if gruz_mother_phase == "charge":
        if gruz_animation_loops == 0 and gruz_mother_frames > 40:
            if not(gruz_charged):
                if gruz_to_knight_direction == "l":
                    gruz_x = -12
                elif gruz_to_knight_direction == "r":
                    gruz_x = 12
                if (knight.y - gruz_mother.y) > 0 and (knight.y - gruz_mother.y) <= 157.5:
                    gruz_y = 5
                elif (knight.y - gruz_mother.y) <= 0 and (knight.y - gruz_mother.y) >= -157.5:
                    gruz_y = -5
                elif (knight.y - gruz_mother.y) > 157.5 and (knight.y - gruz_mother.y) <= 630:
                    gruz_y = 7
                gruz_charged = True
        elif gruz_animation_loops == 1:
            gruz_charged = False

    if not(gruz_health < 0) and not(gruz_mother_phase == "sleeping") and not(gruz_mother_phase == "wakeup"):
        gruz_mother.x += gruz_x
        gruz_mother.y += gruz_y



def hornet_animation():
    global hornet, hornet_animation_frames
    hornet_animation_frames += 1
    if knight.x >= hornet.x + 15:
        if chat_lock and current_line < 2:
            if hornet_animation_frames > 0 and hornet_animation_frames <= 10:
                hornet.image = "hornet/attack/1r"
            elif hornet_animation_frames > 10 and hornet_animation_frames <= 20:
                hornet.image = "hornet/attack/2r"
            elif hornet_animation_frames > 20 and hornet_animation_frames <= 30:
                hornet.image = "hornet/attack/3r"
            elif hornet_animation_frames > 30 and hornet_animation_frames <= 40:
                hornet.image = "hornet/attack/4r"
            elif hornet_animation_frames > 40 and hornet_animation_frames <= 50:
                hornet.image = "hornet/attack/5r"
            elif hornet_animation_frames > 50:
                hornet_animation_frames = 1
        else:
            hornet.image = "hornet/idle/hornet_idle_r"
    elif knight.x <= hornet.x - 15:
        if chat_lock and current_line < 2:
            if hornet_animation_frames > 0 and hornet_animation_frames <= 10:
                hornet.image = "hornet/attack/1l"
            elif hornet_animation_frames > 10 and hornet_animation_frames <= 20:
                hornet.image = "hornet/attack/2l"
            elif hornet_animation_frames > 20 and hornet_animation_frames <= 30:
                hornet.image = "hornet/attack/3l"
            elif hornet_animation_frames > 30 and hornet_animation_frames <= 40:
                hornet.image = "hornet/attack/4l"
            elif hornet_animation_frames > 40 and hornet_animation_frames <= 50:
                hornet.image = "hornet/attack/5l"
            elif hornet_animation_frames > 50:
                hornet_animation_frames = 1
        else:
            hornet.image = "hornet/idle/hornet_idle_l"
            

# event handler function to update the game
# continuously runs
def update():
    global direction, falling_time, stunned, stunned_wait_time, jump_time, touched_ground, jumped, attacked, attack_cooldown, cooldown_time, current_level, level_changed # global variables
    global left_border, right_border, scene1_bg1, scene1_bg2, scene1_door, tutorial_door, hornet, interact_key, bossfight_door, gruz_mother, hit_cooldown, chat_lock, slash
    global hit_cooldown_time, floor2, floor, gruz_mother_phase, gruz_phase_time, gruz_health, music_changed
    global MAX_MOVEMENT, ATTACK_COOLDOWN_TIME # global variables/constants
    gruz_mother_animation()

    hornet_animation()

    gruz_mother_fight()
    
    if music_changed:
        if current_level == "birth":
            music.play("tutorialmp")
            music_changed = False
        elif current_level == "bossfight":
            music.stop()
            music.play("hornetmp")
            music_changed = False
            
    for i in enemies:
        if i == gruz_mother and slash.colliderect(i) and gruz_mother_phase == "sleeping":
            gruz_mother_phase = "wakeup"
            gruz_mother.y -= 50
            music_changed = True

    for i in enemies:
        if knight.colliderect(i) and not(hit_cooldown) and not(gruz_mother_phase == "sleeping"):
            hit(i)

    if knight.colliderect(hornet) or knight.colliderect(scene1_door) or knight.colliderect(tutorial_door) or knight.colliderect(bossfight_door):
        interact_key.pos = (knight.x, knight.y - 80)
    else:
        interact_key.pos = (-50, -50)

    if current_level == "birth":
        if knight.y > 720:
            current_level = "tutorial"
            scene1_door.pos = (-50, -50)
            tutorial_door.pos = (1200, 637)
            floor.pos = (0, 720)
            hornet.pos = (400, 637)
            knight.pos = (540, 0)

    if level_changed:
        if current_level == "scene1":
            floor.pos = (0, 720)
            floor2.pos = (1280, 720)
            knight.pos = (100, 630)
            scene1_door.pos = (50, 637)
            tutorial_door.pos = (-50, -50)
            bossfight_door.pos = (2400, 637)
            hornet.pos = (-50, -50)
            level_changed = False
        elif current_level == "tutorial":
            knight.pos = (1200, 637)
            scene1_door.pos = (-50, -50)
            tutorial_door.pos = (1200, 637)
            bossfight_door.pos = (-50, -50)
            hornet.pos = (400, 637)
            floor.pos = (0, 720)
            floor2.pos = (-200, -200)
            level_changed = False
        elif current_level == "bossfight":
            floor.pos = (0, 720)
            floor2.pos = (-200, -200)
            bossfight_door.pos = (-50, -50)
            knight.pos = (100, 630)
            gruz_mother.pos = (640, 637)
            level_changed = False

    # when the player is not attacking or jumping or falling/landing, the idle animation function is called so the player is set to the idle image
    if not(attacked) and not(jumped) and not(falling_time > 30) and current_level != "birth":
        idle_animation()

    # when the player attack has a cooldown
    if attack_cooldown:
        cooldown_time += 1 # add one to the cooldown timer
        if cooldown_time >= ATTACK_COOLDOWN_TIME: # if the cooldown timer is equal to or bigger than the set attack cooldown time
            cooldown_time = 0 # reset the cooldown timer to 0
            attack_cooldown = False # put attacking off cooldown

    if hit_cooldown:
        hit_cooldown_time += 1
        if hit_cooldown_time >= HIT_COOLDOWN_TIME:
            hit_cooldown_time = 0
            hit_cooldown = False

    # when the user attacks
    if attacked:
        attack_animation() # calls the attack_animation function to animate the player while attacking
        if attack_frame == 10:
            slash.pos = (-1000, -1000)
            attack_cooldown = True # puts the player attacking on cooldown

    # if the jump time is greater than one, then that means the player jumped and is in the air
    # continuously call the jump function and animation
    if jump_time >= 1:
        jump()
        jump_animation()

    # when the player is stunned
    if stunned:
        if abs(time.time()) >= stunned_wait_time + 1: # if one or more seconds passed after the time of the stun
            stunned = False # the player won't be stunned anymore

    if touched_ground and not(stunned):
        falling_time = 0

    # Character Movement
    # if the player is not stunned, to prevent moving when they are stunned
    if not (stunned) and not(chat_lock):
        # when the player holds the left or right key
        # the direction is changed corresponding to the direction they are facing
        # the running_animation function is called to animate the player running
        # the player will move either left or right depending on which direction
        if keyboard.left:
            if current_level == "scene1":
                if knight.x <= 300 and scene1_bg1.x != 0:
                    direction = "left"
                    running_animation()
                    bossfight_door.x += MAX_MOVEMENT
                    scene1_door.x += MAX_MOVEMENT
                    scene1_bg1.x += MAX_MOVEMENT
                    scene1_bg2.x += MAX_MOVEMENT
                    floor.x += MAX_MOVEMENT
                    floor2.x += MAX_MOVEMENT
                else:
                    direction = "left"
                    running_animation()
                    knight.x -= MAX_MOVEMENT
            else:
                direction = "left"
                running_animation()
                knight.x -= MAX_MOVEMENT

        if keyboard.right:
            if current_level == "scene1":
                if knight.x >= 1280 - 300 and scene1_bg2.x != 0:
                    direction = "right"
                    running_animation()
                    bossfight_door.x -= MAX_MOVEMENT
                    scene1_door.x -= MAX_MOVEMENT
                    scene1_bg1.x -= MAX_MOVEMENT
                    scene1_bg2.x -= MAX_MOVEMENT
                    floor.x -= MAX_MOVEMENT
                    floor2.x -= MAX_MOVEMENT
                else:
                    direction = "right"
                    running_animation()
                    knight.x += MAX_MOVEMENT
            else:
                direction = "right"
                running_animation()
                knight.x += MAX_MOVEMENT


    # Collision
    # Gravity / Ground Collision
    # when the player is not touching/colliding with the floor and not jumping, gravity is applied to the player
    #   the player will move depending on the return value of the function character_gravity
    #   the fall_animation function is called to animate the player falling
    # if the player is touching the floor
    # touched_ground will be set to True meaning the player has touched the ground
    # if the falling_time was bigger than 30 then the player will have a "bad landing"
    # the function landing_animation will have a parameter passed through depending on if it was a bad landing or not
    # if
    if not(knight.colliderect(floor)) and not(knight.colliderect(floor2)):
        if not(jumped):
            knight.y += character_gravity()
            fall_animation()
    elif knight.colliderect(floor) or knight.colliderect(floor2):
        touched_ground = True
        if falling_time > 0 and falling_time <= 30:
            landing_animation(False)
        elif falling_time > 30:
            landing_animation(True)


    # border collision
    if knight.x <= left_border:
        knight.x = left_border + 1
    elif knight.x >= right_border:
        knight.x = right_border - 1








pgzrun.go() # run pygame zero
