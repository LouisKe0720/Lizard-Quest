level = 1
current_exp = 0
exp_needed = 100

#Amount of experience gained
def exp(n):
    exp = 5 * (1.7 ** n)
    current_exp += exp
    level()

#Leveling System
def level(current_exp):
    if level != 25:
        #Increase level
        while current_exp > exp_needed:
            current_exp -= exp_needed
            exp_needed = 100 * (1.2 ** level)
            level += 1
            return level
        #Ignore
        while current_exp < exp_needed:
            return level
exp(100)
print(current_exp)
exp(100)
print(level)

