import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame.time import *
import random
import mechanics
import time

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
grass = (34, 139, 34)

# Screen Settings
screen_width, screen_height = 600, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load('LQ LOGO.png'))
pygame.display.set_caption("Lizard Quest")
screen.fill(white)


# Clock and Font
font = pygame.font.SysFont('Arial', 30)
font2 = pygame.font.SysFont('Arial', 50)
font3 = pygame.font.SysFont('Arial', 17)
clock = pygame.time.Clock()

x = 300
y = 380
dx = 500
dy = 380
speed = 5

# Define buttons
start_button = pygame.Rect(20, 170, 400, 75)
time_button = pygame.Rect(20, 370, 400, 75)
back_button = pygame.Rect(300, 370, 100, 75)
skill_button = pygame.Rect(5, 285, 110, 40)
items_button = pygame.Rect(5, 330, 110, 40)
flee_button = pygame.Rect(5, 373, 110, 40)
yes_button = pygame.Rect(140, 358, 130, 60)
no_button = pygame.Rect(280, 358, 130, 60)
gun_button = pygame.Rect(135, 285, 270, 30)
lizard_punch_button = pygame.Rect(135, 315, 270, 30)
magic_punch_button = pygame.Rect(135, 350, 270, 30)
heal_hp_button = pygame.Rect(135, 390, 270, 30)

door = pygame.Rect(70, 0, 50, 400)

# Load battle screen images
battle_screen = pygame.image.load("BASE BATTLE SCREEN.png")
battle_screen = pygame.transform.scale(battle_screen, (screen_width, screen_height))
skills_image = pygame.image.load('SKILLS DESCRIPTIONS - OVERLAY.png')
items_image = pygame.image.load('ITEM DESCRIPTIONS - BASE.png')
flee_image = pygame.image.load('FLEE CHOICES.png')
defenseUpPotion_image = pygame.image.load('ITEM DESCRIPTIONS - DEFENSE UP!.png')
fleePotion_image = pygame.image.load('ITEM DESCRIPTIONS - FLEE POTION.png')
healOrb_image = pygame.image.load('ITEM DESCRIPTIONS - HEAL ORB.png')
magicUpPotion_image = pygame.image.load('ITEM DESCRIPTIONS - MAGIC UP!.png')        
flee_image = pygame.image.load('FLEE CHOICES.png')
flee_success_image = pygame.image.load("FLEE SUCCESS.png")
flee_fail_image = pygame.image.load("FLEE FAIL.png")

dialogueBox = pygame.Rect(135, 300, 440, 100)
dialogueBoxOutline = pygame.Rect(130, 295, 450, 110)
player_battle_rectangle = pygame.Rect(5, 5, 150, 150)
player_battle_rectangle_outline = pygame.Rect(0, 0, 160, 160)


#MUSIC START
pygame.mixer.music.load("DQ Overture XI.mp3")
pygame.mixer.music.set_volume(0.5) 
pygame.mixer.music.play(-1)

class FallingPixel:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-40, screen_height)
        self.speed = random.randint(6, 15)

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, black, (self.x, self.y, 20, 20))

def screen_cover(surface, cover_height):
    pygame.draw.rect(surface, (150, 150, 150), (0, -5, screen_width, cover_height + 55))
    pygame.draw.rect(surface, (100, 100, 100), (0, -10, screen_width, cover_height + 50))
    pygame.draw.rect(surface, (50, 50, 50), (0, -20, screen_width, cover_height + 40))
    pygame.draw.rect(surface, black, (0, 0, screen_width, cover_height))

p_block = pygame.image.load("PURPLE BLOCK TEXTURE.png")
p_block = pygame.transform.scale(p_block, (22, 22))
p_region = pygame.image.load("PURPLE REGION TEXTURE.png")
p_water = pygame.image.load("WATER TEXTURE.png")

def draw_grass(surface, pixel_spacing):
    for i in range(0, screen_width, pixel_spacing):
        for j in range(0, screen_height, pixel_spacing):
            surface.blit(p_region, (i, j))

def draw_block(surface, x, y, final_x, final_y, pixel_spacing=20):
    for i in range(x, final_x, pixel_spacing):
        for j in range(y, final_y, pixel_spacing):
            surface.blit(p_block, (i, j))

pixel_spacing = 30

def background(surface):
    pygame.draw.rect(surface, (105, 201, 97), (0, 0, screen_width, screen_height))
    draw_grass(screen, 15)

    block_positions = [
        (540, 300, 540 + 90, screen_height), (450, 360, 450 + 90, screen_height), (390, 420, 390 + 90, screen_height), (0, 0, 90, 120),
        (0, 0, 45, 200), (0, 0, 20, 300)
    ]

    for x, y, final_x, final_y in block_positions:
        draw_block(screen, x, y, final_x, final_y)

num_pixels = 37
falling_pixels = [FallingPixel() for i in range(num_pixels)]

cover_height = 0
pixel_falling = True

class ImageSprite(Sprite):
    def __init__(self, filename):
        Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, x, y):
        self.rect.center = (x, y)

mutants = [ImageSprite('MUTANT 1.png'), ImageSprite('MUTANT 2.png'), ImageSprite('MUTANT 3.png'), ImageSprite('MUTANT 4.png'),
           ImageSprite('MUTANT 5.png'), ImageSprite('MUTANT 6.png'), ImageSprite('MUTANT 7.png')]
mutant = random.choice(mutants)

frame_1 = ImageSprite('PIXEL TEST F1.png')
frame_2 = ImageSprite('PIXEL TEST F2.png')
frame_3 = ImageSprite('PIXEL TEST F3.png')

mother = ImageSprite('NO GUN 1.png')

frames = [frame_1, frame_2, frame_3]

frame_num = 0
frame_count = 0
frame_change = 5

sprite = frame_1
sprite_group = Group(sprite, mutant)
sprite2_group = Group(sprite, mother)

battle_cg = pygame.transform.scale(pygame.image.load("STORY BATTLE CG.png"), (screen_width, screen_height))
spark_cg = pygame.transform.scale(pygame.image.load("STORY BATTLE SPARK CG.png"), (screen_width, screen_height))
black_bg = pygame.image.load("BLACK BG.png")
cave_bg = pygame.image.load("CAVE BG.png")

dialogue_box = pygame.image.load("DIALOGUE BOX 1.png")
dialogue_box = pygame.transform.scale(dialogue_box, (screen_width, screen_height))

def show_title_screen():
    title_image = pygame.image.load('LQ TITLE SCREEN.png')
    title_image = pygame.transform.scale(title_image, (screen_width, screen_height))
    screen.blit(title_image, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
def show_start_screen():
    start_image = pygame.image.load('LQ START SCREEN.png')
    start_image = pygame.transform.scale(start_image, (screen_width, screen_height))
    waiting = True
    while waiting:
        pygame.draw.rect(screen, white, start_button)
        pygame.draw.rect(screen, white, time_button)
        screen.blit(start_image, (0, 0))  # Redraw the start image
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False
                elif time_button.collidepoint(event.pos):
                    show_time_rectangle()
        pygame.display.flip()

def show_time_rectangle():
    time_waiting = True
    while time_waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                time_waiting = False
        
        time_text = mechanics.time_elapsed()
        text_rect = pygame.Rect(screen_width / 2 - 160, screen_height / 2, 320, 50)
        black_outline = pygame.Rect(screen_width / 2 - 162, screen_height / 2 - 2, 324, 54)
        pygame.draw.rect(screen, black, black_outline)
        pygame.draw.rect(screen, white, text_rect)
        rendered_text = font.render(time_text, True, black)
        screen.blit(rendered_text, (text_rect.x + 10, text_rect.y + 10))
        
        pygame.display.flip()
        clock.tick(60)

def show_battle_screen():
    global dialogue_order, player_health, player_magicPoints, player_level, player_name_text, player_health_text, player_magicpoint_text, player_magicpoint_text2, player_level_text, died, win
    dialogue_order = 1
    died = 0
    win = 0
    defenseUpPotion, fleePotion, healOrb, magicUpPotion = mechanics.item_appear()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skill_button.collidepoint(event.pos):
                    show_skills_screen()
                elif items_button.collidepoint(event.pos):
                    show_items_screen(defenseUpPotion, fleePotion, healOrb, magicUpPotion)
                elif flee_button.collidepoint(event.pos):
                    if not show_flee_screen():
                        waiting = False
        
        if died or win == 1:
            waiting = False
        else:   
            draw_buttons()

            # Enemy 
            global enemy
            enemy = mutant
            enemy.image = pygame.transform.scale(enemy.image, (200, 200))
            default_battle_screen()
            
        pygame.display.update()
    pygame.display.update()

def default_battle_screen():
    # Character Description Formating
    global player_health, player_magicPoints, player_level, monster_health, died, lose, win
    player_health, player_magicPoints, player_level, monster_health = mechanics.display()
    lose = 0
    win = 0

    if player_health <= 0:
        player_health = "000"
        died = 1
    if died != 1:
        if int(player_health) < 100:
            player_health = "0" + str(player_health)
            if int(player_health) < 10:
                player_health = "0" + str(player_health)
    if player_magicPoints < 0:
        player_magicPoints = "000" 
    else:
        if player_magicPoints < 100:
            player_magicPoints = "0" + str(player_magicPoints)
            if int(player_magicPoints) < 10:
                player_magicPoints = "0" + str(player_magicPoints)

    if player_level < 100:
        player_level = "0" + str(player_level)
        if int(player_level) < 10:
            player_level = "0" + str(player_level)

    # Character Description Text
    player_name_text = player_name = font.render("     YOU", True, black)
    player_health_text = font.render("HP:    " + player_health, True, black)
    player_magicpoint_text = font.render("MP:", True, black)
    player_magicpoint_text2 = font.render(player_magicPoints, True, black)
    player_level_text = font.render("LV:     " + player_level, True, black)
    screen.blit(battle_screen, (0, 0))

    pygame.draw.rect(screen, black, player_battle_rectangle_outline)
    pygame.draw.rect(screen, white, player_battle_rectangle)

    screen.blit(player_name_text, (10, 15))
    screen.blit(player_health_text, (10, 60))
    screen.blit(player_magicpoint_text, (10, 90))
    screen.blit(player_level_text, (10, 120))
    screen.blit(player_magicpoint_text2, (91, 90))
    screen.blit(enemy.image, (screen_width / 2 - 80, screen_height / 2 - 150))
    if died == 1:
        dialogue_format("You lost all your health!")
        dialogue_format("You died!")
        dialogue_format("Try again later!")
        lose = 1
    if monster_health <= 0:
        win = 1
    if win == 1:
        dialogue_format("The monster died!")
        dialogue_format("You win the battle!")
    pygame.display.update()

def draw_buttons():
    pygame.draw.rect(screen, white, skill_button)
    pygame.draw.rect(screen, white, items_button)
    pygame.draw.rect(screen, white, flee_button)

def show_flee_screen():
    flee_opened = True
    while flee_opened:
        pygame.draw.rect(screen, white, yes_button)
        pygame.draw.rect(screen, white, no_button)
        screen.blit(flee_image, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flee_button.collidepoint(event.pos) or skill_button.collidepoint(event.pos) or items_button.collidepoint(event.pos):
                    flee_opened = False
                if yes_button.collidepoint(event.pos):
                    if random.choice([True, False]):  
                        success_opened = True
                        while success_opened:
                            screen.blit(flee_success_image, (0, 0))
                            pygame.display.flip()
                            clock.tick(60)
                            pygame.time.wait(2000)
                            win = 1
                            success_opened = False
                            flee_opened = False
                            return False  
                    else:
                        fail_opened = True
                        while fail_opened:
                            screen.blit(flee_fail_image, (0, 0))
                            pygame.display.flip()
                            pygame.time.wait(1000)  # Wait for 1 second
                            fail_opened = False
                            flee_opened = False                
                elif no_button.collidepoint(event.pos):
                    flee_opened = False
    return True
def show_items_screen(defenseUpPotion, fleePotion, healOrb, magicUpPotion):
    items_opened = True
    while items_opened:
        screen.blit(items_image, (0, 0))
        if defenseUpPotion > 0:
            screen.blit(defenseUpPotion_image, (0, 0))
        if fleePotion > 0:
            screen.blit(fleePotion_image, (0, 0))
        if healOrb > 0:
            screen.blit(healOrb_image, (0, 0))
        if magicUpPotion > 0:
            screen.blit(magicUpPotion_image, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if items_button.collidepoint(event.pos) or skill_button.collidepoint(event.pos) or flee_button.collidepoint(event.pos):
                    items_opened = False

def show_skills_screen():
    global dialogue_order, player_magicPoints, win
    skills_opened = True
    gun_used = 0
    magic_punch_used = 0
    heal_hp_used = 0
    lizard_punch_used = 0
    mp_dialogue = 0

    while skills_opened:
        global magic_attack
        magic_attack = 0
        pygame.draw.rect(screen, white, gun_button)
        pygame.draw.rect(screen, white, lizard_punch_button)
        pygame.draw.rect(screen, white, magic_punch_button)
        pygame.draw.rect(screen, white, heal_hp_button)
        screen.blit(skills_image, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skill_button.collidepoint(event.pos) or items_button.collidepoint(event.pos) or flee_button.collidepoint(event.pos):
                    skills_opened = False
                if gun_button.collidepoint(event.pos):
                    skills_opened = False
                    gun_used = 1
                if magic_punch_button.collidepoint(event.pos):
                    if int(player_magicPoints) < 10:
                        skills_opened = False
                        mp_dialogue = 1
                    else:
                        skills_opened = False
                        magic_punch_used = 1
                if lizard_punch_button.collidepoint(event.pos):
                    skills_opened = False
                    lizard_punch_used = 1
                if heal_hp_button.collidepoint(event.pos):
                    if int(player_magicPoints) < 15:
                        skills_opened = False
                        mp_dialogue = 1
                    else:
                        skills_opened = False
                        heal_hp_used = 1

    while gun_used == 1:
        gun_attack()
        gun_used = 0
        
    while magic_punch_used == 1:
        magic_punch()
        magic_punch_used = 0

    while lizard_punch_used == 1:
        lizard_punch()
        lizard_punch_used = 0
        
    while heal_hp_used == 1:
        heal_hp()
        heal_hp_used = 0

    while mp_dialogue == 1:
        default_battle_screen()
        dialogue_format("Not enough MP!")
        mp_dialogue = 0

def heal_hp():
    global dialogue_order
    heal = mechanics.heal_hp()
    default_battle_screen()
    dialogue_order = 10
    battle_dialogue()
    monster_turn()

def lizard_punch():
    global died, win, dialogue_order
    damage = mechanics.lizard_punch()
    player_turn(damage)
    if win != 1:
        dialogue_order = 12
        battle_dialogue()
        dialogue_format("You lost 10 hp from your attack!")
        monster_turn()

def magic_punch():
    global win, dialogue_order, magic_attack
    damage = mechanics.magic_punch()
    magic_attack = 1
    player_turn(damage)
    if win != 1:
        dialogue_order = 8
        battle_dialogue()
        monster_turn()

def gun_attack():
    global win, dialogue_order
    damage = mechanics.use_gun()
    player_turn(damage)
    if win != 1:
        dialogue_order = 6
        battle_dialogue()
        monster_turn()

def player_turn(damage):
    global died, magic_attack, win
    default_battle_screen()
    if died != 1 and win != 1:
        if damage < 10:
            damage = "00" + str(damage)
        monster_lost_health_text = font2.render("- " + damage, True, white)
        text_x = enemy.rect.centerx / 2 + 15
        text_y = enemy.rect.top - 115
        screen.blit(monster_lost_health_text, (text_x, text_y))
        if magic_attack != 1:
            attack_sound()
        elif magic_attack == 1:
            attack_sound2()
            magic_attack = 0
        
def monster_turn():
    global dialogue_order
    default_battle_screen()
    monster_damage = mechanics.monster_attack()
    dialogue_order = 4
    take_damage_sound()
    battle_dialogue()
    dialogue_format("You lost " + str(monster_damage) + " hp!")
    mechanics.regen_mp()
    default_battle_screen()

def attack_sound():
    sound = pygame.mixer.Sound("DQ Attack.mp3")
    sound.play()

def attack_sound2():
    sound = pygame.mixer.Sound("DQ Spell.mp3")
    sound.play()

def take_damage_sound():
    sound = pygame.mixer.Sound("DQ Take Dmg.mp3")
    sound.play()

def battle_dialogue():
    global dialogue_order
    if dialogue_order == 1:
        dialogue_format("You encountered a mutant!")
        dialogue_order = 2

    if dialogue_order == 2:
        dialogue_format("What do you want to do?")
        dialogue_order = 3

    if dialogue_order == 4:
        dialogue_format("The mutant attacked you!")
        dialogue_order = 5

    if dialogue_order == 6:
        dialogue_format("You used your gun!")
        dialogue_order = 7
    
    if dialogue_order == 8:
        dialogue_format("You used magic punch!")
        dialogue_order = 9

    if dialogue_order == 10:
        dialogue_format("You used heal!")
        dialogue_order = 11

    if dialogue_order == 12:
        dialogue_format("You used lizard punch!")
        dialogue_order = 13

def dialogue_format(text):
    global dialogue_order
    pygame.draw.rect(screen, black, dialogueBoxOutline)
    pygame.draw.rect(screen, white, dialogueBox)
    dialogue_text = font.render(text, True, black)
    text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
    screen.blit(dialogue_text, text_rect.topleft)
    pygame.display.flip()
    pygame.time.wait(1500)
    dialogue_order += 1

def show_dialogue_box():
    dialogue_box = pygame.image.load("DIALOGUE BOX 1.png")
    dialogue_box = pygame.transform.scale(dialogue_box, (screen_width, screen_height))
    
    dialogue_surface = pygame.Surface((screen_width, screen_height))
    dialogue_surface.blit(dialogue_box, (0, 0))
    alpha = 0
    fade_time = 60
    
    while alpha < 255:
        dialogue_surface.set_alpha(alpha)
        screen.fill(black)
        screen.blit(dialogue_surface, (0, 0))
        pygame.display.flip()
        alpha += 255 // fade_time
        clock.tick(60)

def show_cg(cg):
    display_cg = cg
    display_cg = pygame.transform.scale(cg, (screen_width, screen_height))
    
    cg_surface = pygame.Surface((screen_width, screen_height))
    cg_surface.blit(display_cg, (0, 0))
    alpha = 0
    fade_time = 60
    
    while alpha < 255:
        cg_surface.set_alpha(alpha)
        screen.fill(black)
        screen.blit(cg_surface, (0, 0))
        pygame.display.flip()
        alpha += 255 // fade_time
        clock.tick(60)

def dialogue(text, text_x, text_y):
    rendered_text = font3.render(text, True, white)
    screen.blit(rendered_text, (text_x, text_y))

mechanics.start_stopwatch()  
show_title_screen()
show_start_screen()
time.sleep(1)
show_dialogue_box()
pygame.mixer.music.load("DQ Adventure Theme.mp3")
pygame.mixer.music.play(-1)

direction = None
moving = False
running = True
start = False
battle_screen_shown = False
cg1 = True
cg1_show = False
cg2 = False
cg2_show = False
text = ""
first_s = True
sec_s = False
story_ms = True
cave_cg = False
scene = "cave"

while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    # First cutscene (cg1)
    while first_s:
        screen.blit(black_bg, (0, 0))
        screen.blit(dialogue_box, (0, 0))
        dialogue("*CRASH*", 258, 402)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_cg(battle_cg)
                cg1 = True
                first_s = False

    while cg1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        cg1_show = True
        text_num = 0
        texts = [
            "Lizard 1: The mutant king shot THE orb?!", "Lizard 2: WHAT!? OUR KING IS BARELY HOLDIN’ UP!", "*BANG*",
            "Lizard King: AHHH!!!!!", "MC lizard: FATHER!", "Lizard 1: THEY GOT THE KING!", "Mutant: KNEEL BEFORE OUR KING’S POWER!",
            "Lizard King: …Hey kiddo.", "MC: DON’T TALK!! I’LL GET SUPPLIES TO STOP THE BLEEDING!",
            "Lizard King: You may not understand what I’m about to say to you but…", "Lizard King: …When the time comes…",
            "Lizard King: Avenge for us ol’ lizards, ok?", "MC: STOP TALKING AS IF YOU’RE GOING TO DIE!",
            "Lizard King: …Keep yourself alive until then, little guy.", "Lizard King: That weird-lookin’ matter won’t keep itself from you.",
            "Lizard King: …", "Lizard King: I think…", "Mutant: I SAID KNEEL BEFORE THE KING’S POWER!",
            "Lizard King: …you may just be the one to succee.…"
        ]
        texts_x = [150, 100, 260, 230, 225, 195, 120, 210, 42, 26, 170, 150, 110, 105, 70, 240, 220, 100, 120]

        while cg1_show and text_num < len(texts):
            screen.blit(battle_cg, (0, 0))
            screen.blit(dialogue_box, (0, 0))
            dialogue(texts[text_num], texts_x[text_num], 403)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    text_num += 1
                    if text_num >= len(texts):
                        cg1_show = False
                        cg1 = False
                        cg2 = True
                        sec_s = True
                        show_cg(spark_cg)
                        text2_num = 0

    if cg2:
        if sec_s:
            screen.blit(spark_cg, (0, 0))
            screen.blit(dialogue_box, (0, 0))
            dialogue("!!!", 290, 402)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                sec_s = False
                cg2_show = True
                text2_num = 0
                texts2 = ["!!!", "MC: FATHER!!!"]
                texts2_x = [290, 230]

                while cg2_show and text2_num < len(texts2):
                    screen.blit(spark_cg, (0, 0))
                    screen.blit(dialogue_box, (0, 0))
                    dialogue(texts2[text2_num], texts2_x[text2_num], 402)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            text2_num += 1
                            if text2_num >= len(texts2):
                                cg2_show = False
                                cg2 = False
                                cave_cg = True
                                cave_s = True

    if cave_cg:
        screen.blit(cave_bg, (0, 0))
        screen.blit(dialogue_box, (0, 0))
        textc_num = 0
        texts_c = [
            "MC: ...!", "Motherly lizard: You’re up!", "Motherly lizard: You’re sweating all over… are you alright?", "MC: …",
            "Motherly lizard: Well… I understand that you’re nervous for today…", "Motherly lizard: …", "Motherly lizard: Are you sure you want to do this?",
            "MC: …Yes.", "MC: I must avenge fathe-, I mean, our beloved lizard king,", "MC: who fought all those stupid mutants out there just to protect me.",
            "MC: I must show that oh-so mighty king", "MC: who dared to kill our beloved lizard king that...",
            "MC: we are not just some ‘brainless tails’.", "Motherly lizard: I understand your anger and rage but…", 
            "Motherly lizard: … never mind. Your mind must be set.", "Motherly lizard: At the very least,",
            "Motherly lizard: please promise me to keep yourself safe out there", "MC: !!", "Magic gained!",
            "Motherly lizard: I want to see you back here at...", "Motherly lizard: the cave when everything is over.", "MC: …I’ll try my best.",
            "Motherly lizard: Oh, and carry this rifle with you.", "Rifle gained!", "Motherly lizard: …", "MC: …",
            "Motherly lizard: …I hope we can finally avenge those","Motherly Lizard: who fought for us to live here today.", "MC: Of course… that is the sole reason I am doing this.",
            "MC: See you after all of this ends, mum.", "MC: I will make sure that everything ends just the way Dad would’ve wanted."]
        textsc_x = [258, 168, 140, 258, 48, 230, 90, 258, 70, 50, 120, 60, 80, 91, 100, 125, 100, 258, 240, 120, 130, 160, 120, 240, 240, 258, 130, 140, 130, 120, 100, 40]
        while cave_cg and textc_num < len(texts_c):
            screen.blit(dialogue_box, (0, 0))
            dialogue(texts_c[textc_num], textsc_x[textc_num], 402)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    textc_num += 1
                    if textc_num >= len(texts_c):
                        cave_cg = False 
    
    keys = pygame.key.get_pressed()

    if keys[K_a] and x > 0:
        x -= speed
        moving = True
        if direction != 'left':
            frame_count = 0
            direction = 'left'
    elif keys[K_d] and x < screen_width - sprite.rect.width:
        x += speed
        moving = True
        if direction != 'right':
            frame_count = 0
            direction = 'right'
    elif keys[K_w] and y > 0:
        y -= speed
        moving = True
    elif keys[K_s] and y < screen_height - sprite.rect.height:
        y += speed
        moving = True
    else:
        moving = False

    if moving:
        frame_count += 1
        if frame_count >= frame_change:
            frame_count = 0
            frame_num = (frame_num + 1) % len(frames)
            sprite.image = frames[frame_num].image
            if direction == 'left':
                if frame_num != 0:
                    sprite.image = pygame.transform.flip(sprite.image, True, False)
                else:
                    sprite.image = frames[frame_num].image
            else:
                sprite.image = frames[frame_num].image

    sprite.update(x, y)
    mother.update(560, 380)

    if scene == "cave":
        screen.fill(white)
        pygame.draw.rect(screen, white, door)
        screen.blit(cave_bg, (0, 0))
        sprite2_group.draw(screen)

        if sprite.rect.colliderect(door):
            dx, dy = 480, 200 
            x, y = 100, 380 
            sprite.update(x, y)
            mutant.update(dx, dy)
            scene = "main"

    elif scene == "main":
        mutant.update(dx, dy)

        screen.fill(white)
        background(screen)
        sprite_group.draw(screen)

        if sprite.rect.colliderect(mutant.rect):
            pygame.mixer.music.load("DQ Battle Theme SNES.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            speed = 0
            if pixel_falling:
                for pixel in falling_pixels:
                    pixel.fall()
                    pixel.draw(screen)
            if cover_height < screen_height:
                cover_height += 8
            if cover_height == screen_height:
                pixel_falling = False
                battle_screen_shown = True
    
            screen_cover(screen, cover_height)
        
        while pixel_falling == False and battle_screen_shown == True:
            global lose, died
            show_battle_screen()
            if win == 1:
                dx = 1000
                dy = 1000
            elif lose == 1:
                enemy.image = pygame.transform.scale(enemy.image, (100, 100))
                x -= 20
                lose = 0
                died = 0
                win = 0
                cover_height = 0
                pixel_falling = True
                num_pixels = 37
                mechanics.player_health = 30
                mechanics.monster_health = 30
    
            battle_screen_shown = False
            pygame.mixer.music.load("DQ Adventure Theme.mp3")
            pygame.mixer.music.play(-1)
            speed = 5

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
