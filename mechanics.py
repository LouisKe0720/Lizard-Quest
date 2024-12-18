#############################################  MECHANICS  #############################################


#############################################  EXP SYSTEM #############################################

level = 1
current_exp = 0
exp_needed = 100

# Amount of experience gained
def gain_exp(n, current_exp, level, exp_needed):
    exp = 5 * (n ** 1.7)
    current_exp += exp
    return level_up(current_exp, level, exp_needed)

# Leveling System
def level_up(current_exp, level, exp_needed):
    while current_exp >= exp_needed and level < 25:
        current_exp -= exp_needed
        level += 1
        exp_needed = 100 * (1.2 ** level)
    return level, round(current_exp), round(exp_needed)

# Display Level
def level_display(x):
    global current_exp, level, exp_needed
    level, current_exp, exp_needed = gain_exp(x, current_exp, level, exp_needed)
    if level != 25:
        print(f"Level: {level}  EXP Needed: {current_exp}/{exp_needed}")
    else:
        print("Level: 25 (MAX LEVEL)")

#############################################  HEALTH SYSTEM  #############################################

player_health = 15
monster_health = 0

# Player Damage Calculation
def player_damage(damage):
    global player_health
    player_health -= damage
    if player_health <= 0:
        # TRY AGAIN SCREEN
        return

# Monster Health
def monster_health_display(difficulty):
    global monster_health
    monster_health = 5 + (2 * (difficulty + level))

# Monster Damage Calculation
def monster_damage(damage):
    global monster_health
    monster_health -= damage
    if monster_health <= 0:
        # MONSTER DEFEATED SCREEN
        return