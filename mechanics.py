level = 1
current_exp = 0
exp_needed = 100

# Amount of experience gained
def gain_exp(n, current_exp, level, exp_needed):
    exp = 5 * (n ** 1.7)
    current_exp += exp
    return current_exp, level_up(current_exp, level, exp_needed)

# Leveling System
def level_up(current_exp, level, exp_needed):
    while current_exp >= exp_needed and level < 25:
        current_exp -= exp_needed
        level += 1
        exp_needed = 100 * (1.2 ** level)
    current_exp = round(current_exp)
    exp_needed = round(exp_needed)
    return level, current_exp, exp_needed

def level_display(x):
    #TEST
    global current_exp, level, exp_needed
    current_exp, (level, current_exp, exp_needed) = gain_exp(x, current_exp, level, exp_needed)
    if level != 25:
        print(f"Level: {level}  EXP Needed: {current_exp}/{exp_needed}")
    else:
        print("Level: 25 (MAX LEVEL)")

level_display(100)