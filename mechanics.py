level = 1
current_exp = 0
exp_needed = 100

# Amount of experience gained
def gain_exp(n, current_exp, level, exp_needed):
    exp = 5 * (1.7 ** n)
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

def main():
    #TEST
    global current_exp, level, exp_needed
    current_exp, (level, current_exp, exp_needed) = gain_exp(10, current_exp, level, exp_needed)
    print(f"Level: {level}, Current EXP: {current_exp}, EXP Needed: {exp_needed}")

main()