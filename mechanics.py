#############################################    IMPORT   #############################################
import time
import random

#############################################  MECHANICS  #############################################

#############################################  EXP SYSTEM #############################################

level = 1
current_exp = 0
exp_needed = 100

# Amount of experience gained
def gain_exp(n, current_exp, level, exp_needed):
    exp = 5 * (1.7) * n # CAN CHANGE
    current_exp += exp
    while current_exp >= exp_needed and level < 25: #CAN CHANGE MAX LEVEL
        current_exp -= exp_needed
        level += 1
        exp_needed = 100 * (1.2 ** level) # CAN CHANGE
    return level, round(current_exp), round(exp_needed)

# Display Level
def level_display(x): # TAKES IN DIFFICULTY OF MONSTER
    global current_exp, level, exp_needed
    level, current_exp, exp_needed = gain_exp(x, current_exp, level, exp_needed)
    if level != 25: # CAN CHANGE MAX LEVEL
        print(f"Level: {level}  EXP Needed: {current_exp}/{exp_needed}")
    else:
        print("Level: 25 (MAX LEVEL)") # CAN CHANGE MAX LEVEL

#############################################  HEALTH SYSTEM  #############################################

player_health = 15 # CAN CHANGE
monster_health = 0
max_health = 15 # CAN CHANGE

# Player Health calculation
def player_health_display(level):
    global player_health
    global max_health
    player_health = 15 + (2 * (level - 1)) # CAN CHANGE
    max_health = player_health
    return player_health

# Player Damage Calculation
def player_damage(damage): #TAKES IN AN ATTACK DAMAGE
    global player_health
    player_health -= damage
    if player_health <= 0:
        #PLACEHOLDER
        # TRY AGAIN SCREEN
        return 

# Monster Health
def monster_health_display(difficulty): #DIFFICULTY OF THE MONSTER
    global monster_health
    monster_health = 5 + (2 * (difficulty + level)) # CAN CHANGE
    return monster_health

# Monster Damage Calculation
def monster_damage(damage): #TAKES IN AN ATTACK DAMAGE
    global monster_health
    monster_health -= damage
    if monster_health <= 0:
        # PLACEHOLDER
        # MONSTER DEFEATED SCREEN
        return
    
# AUTO HEAL?
def auto_heal(): # CAN ADD TIME TO THIS
    global player_health
    player_health += 1 # CAN CHANGE HOW MUCH TO HEAL
    if player_health > max_health:
        player_health = max_health 
    
#############################################  TIME  #############################################

# START TIME
def start_stopwatch(): # MUST CALL IT AT THE START
    global start_time
    start_time = time.time()

# STOP TIME
def stop_stopwatch(): # DON"T CALL IT, USE TIME ELAPSED
    global start_time
    return time.time() - start_time

# TIME FORMAT
def time_format(time):
    seconds = time % 60
    minutes = (time // 60) % 60
    hours = (time // 60) // 60
    if seconds < 10:
        seconds = f"0{seconds}"
    if minutes < 10:
        minutes = f"0{minutes}"
    if hours < 10:
        hours = f"0{hours}"
    print(f"Time: {hours}:{minutes}:{seconds}") # CAN CHANGE TO BECOME RETURN

# TIME ELAPSED
def time_elapsed():
    play_time = stop_stopwatch()
    play_time = int(play_time) # ROUNDS DOWN TO SECOND
    time_format(play_time)

#############################################  SKILLS  #############################################

# SKILL SYSTEM

# SKILL 1
def skill_1(damage): # CAN CHANGE
    player_damage(damage)

# SKILL 2
def skill_2(damage):
    player_damage(damage)

# SKILL 3
def skill_3(damage):
    player_damage(damage)

# SKILL 4
def skill_4(damage):
    player_damage(damage)

# SKILL 5
def skill_5(damage):
    player_damage(damage)

# CAN ADD MORE SKILLS #############################################

