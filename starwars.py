
"""
    Turtle Graphics - Shooting Game
"""

import turtle, pygame, pygame.midi, time, random
from pygame.locals import *
pygame.init()
pygame.midi.init()
output = pygame.midi.Output(pygame.midi.get_default_output_id())
lasersound = pygame.mixer.Sound('laser.wav')
explosionsound = pygame.mixer.Sound('explosion.wav')
victory = pygame.mixer.Sound('victory.wav')
defeat = pygame.mixer.Sound('defeat.wav')
menumusic = pygame.mixer.Sound('menumusic.wav')
gamemusic = pygame.mixer.Sound('gamemusic.wav')

"""
    Constants and variables
"""

# General parameters
window_height = 600
window_width = 600
window_margin = 50
update_interval = 25    # The screen update interval in ms, which is the
                        # interval of running the updatescreen function 

# Player's parameters
player_size = 50        # The size of the player image plus margin
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10       # The speed the player moves left or right
score = 0

# Enemy's parameters
enemy_number = 18        # The number of enemies in the game

enemy_size = 50         # The size of the enemy image plus margin
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin - 50
enemy_min_x = enemy_init_x
enemy_max_x = window_width / 2 - enemy_size * 7
    # The maximum x coordinate of the first enemy, which will be used
    # to restrict the x coordinates of all other enemies
enemy_hit_player_distance = 50
    # The player will lose the game if the vertical
    # distance between the enemy and the player is smaller
    # than this value

# Enemy movement parameters
enemy_speed = 2
tempenemyspeed = enemy_speed
enemy_speed_increment = 1
    # The increase in speed every time the enemies move
    # across the window and back
enemy_direction = 1
    # The current direction the enemies are moving:
    #     1 means from left to right and
    #     -1 means from right to left

# The list of enemies
enemies = []

# Laser parameter
laser_width = 6
laser_height = 43
laser_speed = 20
laser_hit_enemy_distance = 30
    # The laser will destory an enemy if the distance
    # between the laser and the enemy is smaller than
    # this value

# Bonus parameter
min_spawn_time = 2000
max_spawn_time = 7000
bonus_speed = 2
laser_hit_bonus_distance = 30
returnflag = 0

# Stop key
stopflag = 0


"""
    Handle the player movement
"""

# This function is run when the "Left" key is pressed. The function moves the
# player to the left when the player is within the window area
def playermoveleft():

    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range
    if x - player_speed > -window_width / 2 + window_margin:
        player.goto(x - player_speed, y)


# This function is run when the "Right" key is pressed. The function moves the
# player to the right when the player is within the window area
def playermoveright():

    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range
    if x + player_speed < window_width / 2 - window_margin:
        player.goto(x + player_speed, y)


"""
    Handle the screen update and enemy movement
"""

def stopmovement():
    global stopflag, enemy_speed, bonus_speed
    
    if stopflag % 2 == 0:
        enemy_speed = 0
        bonus_speed = 0
    else:
        enemy_speed = tempenemyspeed
        bonus_speed = 2

    stopflag += 1

# This function is run in a fixed interval. It updates the position of all
# elements on the screen, including the player and the enemies. It also checks
# for the end of game conditions.
def updatescreen():
    # Use the global variables here because we will change them inside this
    # function
    global enemy_direction, enemy_speed, score, tempenemyspeed
    # Move the enemies depending on the moving direction

    # The enemies can only move within an area, which is determined by the
    # position of enemy at the top left corner, enemy_min_x and enemy_max_x

    # x and y displacements for all enemies
    dx = enemy_speed * enemy_direction
    dy = 0

    if enemy_speed != 0:
        tempenemyspeed = enemy_speed

    # Part 3.3
    # Perform several actions if the enemies hit the window border
    x0 = enemies[0].xcor()
    if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:

        # Switch the moving direction
        enemy_direction *= -1

        # Bring the enemies closer to the player
        dy = -enemy_size/2

        # Increase the speed when the direction switches to right again
        if enemy_direction == 1:
            enemy_speed += enemy_speed_increment

    # Move the enemies according to the dx and dy values determined above
    for enemy in enemies:
        x, y = enemy.position()
        enemy.goto(x + dx, y + dy)

        if x//20 % 2 == 0:
            enemy.shape("enemy.gif")
        elif x//20 % 2 == 1:
            enemy.shape("enemy2.gif")

    # Part 4.3 - Moving the laser
    # Perfrom several actions if the laser is visible
    if laser.isvisible():
        # Move the laser
        laser.forward(laser_speed)
        
        # Hide the laser if it goes beyong the window
        if laser.ycor() > window_height / 2:
            laser.hideturtle()
    
        # Check the laser against every enemy using a for loop
        for enemy in enemies:
            # If the laser hits a visible enemy, hide both of them
            if laser.distance(enemy) < laser_hit_enemy_distance  and enemy.isvisible():
                laser.hideturtle()
                enemy.hideturtle()
                explosionsound.play()
                score += 10

                # Stop if some enemy is hit
                break
        
        if laser.distance(bonus) < laser_hit_bonus_distance and bonus.isvisible():
            laser.hideturtle()
            bonus.hideturtle()
            explosionsound.play()
            score += 100

    # Part 5.1 - Gameover when one of the enemies is close to the player

    # If one of the enemies is very close to the player, the game will be over
    for enemy in enemies:
        if enemy.ycor()-player.ycor() < enemy_hit_player_distance and enemy.isvisible():
            # Show a message
            gameover("You lose!")

            # Return and do not run updatescreen() again
            return

    # Part 5.2 - Gameover when you have killed all enemies

    # Set up a variable as a counter
    count = 0

    # For each enemy
    for enemy in enemies:

        # Increase the counter if the enemy is visible
        if enemy.isvisible():
            count += 1

    # If the counter is 0, that means you have killed all enemies
    if count == 0:

        # Perform several gameover actions
        gameover("You win!")
        return

    if not bonus.isvisible():
        def bonusspawn():
            random.seed()
            bonus.goto(350,250)
            bonus.showturtle()
        turtle.ontimer(bonusspawn, random.randint(min_spawn_time, max_spawn_time))
    elif bonus.isvisible():
        if bonus.xcor() <= -350:
            bonus.hideturtle()
        else:
            bonus.backward(bonus_speed)

    score_counter.clear()
    score_counter.goto(-290, 270)
    score_counter.color("white")
    score_counter.write("Score:     {}".format(score), font=("Consolas", 12, "bold"))
    
    # Part 3.1 - Controlling animation using the timer event
    turtle.update()
    turtle.ontimer(updatescreen, update_interval)
    
"""
    Shoot the laser
"""

# This function is run when the player presses the spacebar. It shoots a laser
# by putting the laser in the player's current position. Only one laser can
# be shot at any one time.
def shoot():
    # Part 4.2 - the shooting function
    # Shoot the laser only if it is not visible
    if not laser.isvisible():
        laser.showturtle()
        laser.up()
        laser.goto(player.position())
        lasersound.play()

"""
    Game start
"""

# This function contains things that have to be done when the game starts.
def gamestart(x, y):
    # Use the global variables here because we will change them inside this
    # function
    global player, laser, Consolas, explosion, bonus, score_counter, score

    ### Clear starting screen ###
    pygame.mixer.stop()

    gamemusic.play()
    
    start_button.clear()
    start_button.hideturtle()
    labels.clear()
    labels.hideturtle()
    left_arrow.clear()
    left_arrow.hideturtle()
    right_arrow.clear()
    right_arrow.hideturtle()
    enemy_number_text.clear()
    title.hideturtle()
    title.clear()
    instruction_message.hideturtle()
    instruction_message.clear()


    ### Add background ###
    
    turtle.bgpic('gamebg.gif')

    ### Enemy turtles ###

    # Add the enemy picture
    turtle.addshape("enemy.gif")
    turtle.addshape("enemy2.gif")

    for i in range(enemy_number):
        # Create the turtle for the enemy
        enemy = turtle.Turtle()
        enemy.shape("enemy.gif")
        enemy.up()

        # Move to a proper position counting from the top left corner
        enemy.goto(enemy_init_x + enemy_size * (i % 7), enemy_init_y - enemy_size * (i // 7))

        # Add the enemy to the end of the enemies list
        enemies.append(enemy)

    ### Bonus enemy turtle ###

    turtle.addshape("bonus.gif")
    bonus = turtle.Turtle()
    bonus.shape("bonus.gif")
    bonus.up()
    bonus.hideturtle()
    bonus.goto(350,250)
        
    ### Laser turtle ###

    # Create the laser turtle using the square turtle shape
    turtle.addshape("laser.gif")
    laser = turtle.Turtle()
    laser.shape("laser.gif")

    # Change the size of the turtle and change the orientation of the turtle
    laser.shapesize(laser_width / 20, laser_height / 20)
    laser.left(90)
    laser.up()

    # Hide the laser turtle
    laser.hideturtle()

    # Part 4.2 - Mapping the shooting function to key press event
    turtle.onkeypress(shoot, "space")
    
    turtle.update()

    # Part 3.1 - Controlling animation using the timer event
    turtle.ontimer(updatescreen, update_interval)

    ### Score turtle ###

    score_counter = turtle.Turtle()
    score_counter.up()
    score_counter.hideturtle()
    score_counter.goto(-290, 270)
    score_counter.color("white")
    score_counter.write("Score:    {}".format(score), font=("Consolas", 12, "bold"))

    ### Player turtle ###
    
    # Add the spaceship picture
    turtle.addshape("spaceship.gif")

    # Create the player turtle and move it to the initial position
    player = turtle.Turtle()
    player.shape("spaceship.gif")
    player.up()
    player.goto(player_init_x, player_init_y)

    # Part 2.1
    # Map player movement handlers to key press events

    turtle.onkeypress(playermoveleft, "Left")
    turtle.onkeypress(playermoveright, "Right")
    turtle.onkeypress(stopmovement, "x")
    turtle.listen()


"""
    Game over
"""

# This function shows the game over message.
def gameover(message):

    pygame.mixer.stop()
    
    score_counter.clear()
    score_counter.goto(-290, 270)
    score_counter.color("white")
    score_counter.write("Score:     {}".format(score), font=("Consolas", 12, "bold"))

    # Play win or lose sound
    if message == "You lose!":
        defeat.play()
    elif message == "You win!":
        victory.play()
    
    # Part 5.3 - Improving the gameover() function
    final_message = turtle.Turtle()
    final_message.color("Yellow")
    final_message.hideturtle()
    final_message.write(message, align="center", font=("Consolas", 30, "bold"))
    turtle.update()    

"""
    Set up main Turtle parameters
"""

def decrease_enemy_number(x, y):
    #Declare enemy number as global
    global enemy_number

    if enemy_number > 1:
        #Decrease number of enemies by 1
        enemy_number -= 1

        # Tell the turtle 'enemy_number_text' to clear what it has written
        enemy_number_text.clear()

        # Tell the turtle 'enemy_number_text' to display the new value
        enemy_number_text.write(str(enemy_number), font=("Consolas", 12, "bold"), align="center")

def increase_enemy_number(x, y):
    #Declare enemy number as global
    global enemy_number

    if enemy_number < 49:
        #Increase number of enemies by 1
        enemy_number += 1

        # Tell the turtle 'enemy_number_text' to clear what it has written
        enemy_number_text.clear()

        # Tell the turtle 'enemy_number_text' to display the new value
        enemy_number_text.write(str(enemy_number), font=("Consolas", 12, "bold"), align="center")

# Set up the turtle window
turtle.setup(window_width, window_height)
turtle.bgpic('startbg.gif')
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

menumusic.play()

# Set up start button
start_button = turtle.Turtle()
start_button.onclick(gamestart)
start_button.up()
start_button.goto(-40,-90)
start_button.color("White","DarkGray")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()
start_button.color("White")
start_button.goto(0,-85)
start_button.write("Start", font=("Consolas", 12, "bold"), align = "center")
start_button.goto(0, -78)
start_button.shape("square")
start_button.shapesize(1.25, 4)
start_button.color("")

# Set up title in start screen
title = turtle.Turtle()
title.hideturtle()
title.color("white")
title.up()
title.goto(0,150)
title.write("Python", font=("Consolas", 50, "bold"), align="center")
title.goto(0,80)
title.write("Sith Invasion", font=("Consolas", 50, "bold"), align="center")

# Set up instructions
instruction_message = turtle.Turtle()
instruction_message.color("white")
instruction_message.hideturtle()
instruction_message.up()
instruction_message.goto(0, 50)
instruction_message.write("The Sith TIE Starfigthers are invading!", font=("Consolas", 16, "bold"), align="center")
instruction_message.goto(0, 25)
instruction_message.write("Use the left and right arrow keys to move.", font=("Consolas", 16, "bold"), align="center")
instruction_message.goto(0,0)
instruction_message.write("Use spacebar to shoot.", font=("Consolas", 16, "bold"), align="center")

# Set up spinner control
labels = turtle.Turtle()
labels.hideturtle()
labels.color("white")
labels.up()
labels.goto(-100, -50) # Put the text next to the spinner control
labels.write("Number of TIE starfighters: ", font=("Consolas", 12, "bold"), align = 'center')

enemy_number_text = turtle.Turtle()
enemy_number_text.hideturtle()
enemy_number_text.color("white")
enemy_number_text.up()
enemy_number_text.goto(80,-50)
enemy_number_text.write(str(enemy_number), font=("Consolas", 12, "bold"), align="center")

left_arrow = turtle.Turtle()
left_arrow.color("white")
left_arrow.shape("arrow")
left_arrow.up()
left_arrow.shapesize(0.5, 1)
left_arrow.right(180)
left_arrow.goto(60, -42)
left_arrow.onclick(decrease_enemy_number)

right_arrow = turtle.Turtle()
right_arrow.color("white")
right_arrow.shape("arrow")
right_arrow.up()
right_arrow.shapesize(0.5, 1)
right_arrow.goto(100, -42)
right_arrow.onclick(increase_enemy_number)

turtle.update()

# Switch focus to turtle graphics window
turtle.done()
