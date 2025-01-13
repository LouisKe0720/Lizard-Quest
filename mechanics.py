#############################################    IMPORT   #############################################
import time
import random

#############################################  MECHANICS  #############################################

#############################################  EXP SYSTEM #############################################

player_level = 1
current_exp = 0
exp_needed = 100

# Amount of experience gained
def gain_exp(n, current_exp, player_level, exp_needed):
    exp = 5 * (1.7)**n # CAN CHANGE
    current_exp += exp
    while current_exp >= exp_needed and player_level < 25: #CAN CHANGE MAX LEVEL
        current_exp -= exp_needed
        player_level += 1
        exp_needed = 100 * (1.2 ** player_level) # CAN CHANGE
    return player_level, round(current_exp), round(exp_needed)

# Display Level
def level_display(x): # TAKES IN DIFFICULTY OF MONSTER
    global current_exp, player_level, exp_needed
    player_level, current_exp, exp_needed = gain_exp(x, current_exp, player_level, exp_needed)
    if player_level != 25: # CAN CHANGE MAX LEVEL
        print(f"Level: {player_level}  EXP Needed: {current_exp}/{exp_needed}")
    else:
        print("Level: 25 (MAX LEVEL)") # CAN CHANGE MAX LEVEL

#############################################  HEALTH SYSTEM  #############################################

player_health = 30
monster_health = 30
max_health = 30 
min_player_health = 0
min_monster_health = 0
min_magic_points = 0

# Player Health calculation
def player_health_display(player_level):
    global player_health
    global max_health
    player_health = 31 + (2 * (player_level - 1)) # CAN CHANGE
    max_health = player_health
    return player_health

# Player Damage Calculation
def player_damage(damage): #TAKES IN AN ATTACK DAMAGE
    global player_health
    player_health -= damage
    return 

# Monster Health
def monster_health_display(difficulty): #DIFFICULTY OF THE MONSTER
    global monster_health
    monster_health = 5 + (2 * (difficulty + player_level)) # CAN CHANGE
    return monster_health

# Monster Damage Calculation
def monster_damage(damage): #TAKES IN AN ATTACK DAMAGE
    global monster_health
    monster_health -= damage
    return
    
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
    return str(f"Time Played: {hours}:{minutes}:{seconds}")

# TIME ELAPSED
def time_elapsed():
    play_time = stop_stopwatch()
    play_time = int(play_time) # ROUNDS DOWN TO SECOND
    return time_format(play_time)

#############################################  SKILLS  #############################################
player_magicPoints = 25

# SKILL SYSTEM

# SKILL 1
def use_gun():
    monster_damage(3)
    return 3

# SKILL 2
def lizard_punch():
    global player_health
    player_health -= 10
    monster_damage(7)
    return 7

# SKILL 3
def magic_punch():
    global player_magicPoints 
    player_magicPoints -= 10
    monster_damage(9)
    return 9

# SKILL 4
def heal_hp():
    global player_health
    global max_health
    global player_magicPoints
    player_magicPoints -= 15
    player_health += 5
    if player_health > max_health:
        player_health = max_health


#############################################  MONSTER ATTACKS  #############################################

def monster_attack1():
    player_damage(1)
    return 1

def monster_attack2():
    player_damage(2)
    return 2

def monster_attack3():
    player_damage(3)
    return 3

def monster_attack4():
    player_damage(4)
    return 4

def monster_attack():
    randomMonsterAttack = random.randint(1, 4)
    if randomMonsterAttack == 1:
        return monster_attack1()
    elif randomMonsterAttack == 2:
        return monster_attack2()
    elif randomMonsterAttack == 3:
        return monster_attack3()
    elif randomMonsterAttack == 4:
        return monster_attack4()

############################################### ITEMS #############################################

def item_appear():
    global defenseUpPotion
    global fleePotion
    global healOrb
    global magicUpPotion
    defenseUpPotion = 0
    fleePotion = 0
    healOrb = 0
    magicUpPotion = 0
    return defenseUpPotion, fleePotion, healOrb, magicUpPotion

def gain_defPotion(n):
    global defenseUpPotion
    defenseUpPotion += n

def gain_fleePotion(n):
    global fleePotion
    fleePotion += n

def gain_healOrb(n):
    global healOrb
    healOrb += n

def gain_magicPotion(n):
    global magicUpPotion
    magicUpPotion += n

################################################ BATTLE SCREEN #################################################

def display():
    global player_health
    global player_magicPoints
    global player_level
    global monster_health
    return player_health, player_magicPoints, player_level, monster_health

    