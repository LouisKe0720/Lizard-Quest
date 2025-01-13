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
clock = pygame.time.Clock()

x = 300
y = 220
dx = 500
dy = 220
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

frames = [frame_1, frame_2, frame_3]

frame_num = 0
frame_count = 0
frame_change = 5

sprite = frame_1
sprite_group = Group(sprite, mutant)

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
    global dialogue_order
    dialogue_order = 1
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

        draw_buttons()

        # Battle Screen
        screen.blit(battle_screen, (0, 0))
        player_battle_rectangle = pygame.Rect(5, 5, 150, 150)
        player_battle_rectangle_outline = pygame.Rect(0, 0, 160, 160)
        pygame.draw.rect(screen, black, player_battle_rectangle_outline)
        pygame.draw.rect(screen, white, player_battle_rectangle)

        # Character Description Formating
        player_health, player_magicPoints, player_level = mechanics.display()
        if player_health < 100:
            player_health = "0" + str(player_health)
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

        # Character Description Display
        screen.blit(player_name_text, (10, 15))
        screen.blit(player_health_text, (10, 60))
        screen.blit(player_magicpoint_text, (10, 90))
        screen.blit(player_level_text, (10, 120))
        screen.blit(player_magicpoint_text2, (91, 90))

        # Enemy 
        enemy = mutant
        enemy.image = pygame.transform.scale(enemy.image, (200, 200))
        screen.blit(enemy.image, (screen_width / 2 - 100, screen_height / 2 - 150))
        battle_dialogue()
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
                            success_opened = False
                            flee_opened = False
                            return False  # Return False to close the battle screen
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
    skills_opened = True
    global dialogue_order
    gun_used = 0
    while skills_opened:
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
                    skills_opened = False
                    magic_punch_used = 1
                if heal_hp_button.collidepoint(event.pos):
                    skills_opened = False
                    heal_hp_used = 1

    while gun_used == 1:
        mechanics.use_gun()
        pygame.display.update()
        dialogue_order = 6
        battle_dialogue()
        mechanics.monster_attack()
        dialogue_order = 4
        battle_dialogue()
        gun_used = 0

        pygame.display.update()
    
    while magic_punch_used == 1:
        mechanics.magic_punch()
        pygame.display.update()
        dialogue_order = 8
        battle_dialogue()
        mechanics.monster_attack()
        dialogue_order = 4
        battle_dialogue()
        magic_punch_used = 0 
        pygame.display.update()

    while heal_hp_used == 1:
        mechanics.heal_hp
        pygame.display.update()
        dialogue_order = 10
        battle_dialogue()
        mechanics.monster_attack()
        dialogue_order = 4
        battle_dialogue()
        heal_hp_used = 0
        pygame.display.update()

def battle_dialogue():
    global dialogue_order
    dialogueBox = pygame.Rect(135, 300, 440, 100)
    dialogueBoxOutline = pygame.Rect(130, 295, 450, 110)
    if dialogue_order == 1:
        pygame.draw.rect(screen, black, dialogueBoxOutline)
        pygame.draw.rect(screen, white, dialogueBox)
        dialogue_text = font.render("You encountered a mutant!", True, black)
        text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
        screen.blit(dialogue_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(2000)
        dialogue_order += 1

    if dialogue_order == 2:
        pygame.draw.rect(screen, black, dialogueBoxOutline)
        pygame.draw.rect(screen, white, dialogueBox)
        dialogue_text = font.render("What do you want to do?", True, black)
        text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
        screen.blit(dialogue_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(2000)
        dialogue_order += 1

    if dialogue_order == 4:
        pygame.draw.rect(screen, black, dialogueBoxOutline)
        pygame.draw.rect(screen, white, dialogueBox)
        dialogue_text = font.render("The mutant punched you", True, black)
        text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
        screen.blit(dialogue_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(2000)
        dialogue_order += 1

    if dialogue_order == 6:
        pygame.draw.rect(screen, black, dialogueBoxOutline)
        pygame.draw.rect(screen, white, dialogueBox)
        dialogue_text = font.render("You used your gun!", True, black)
        text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
        screen.blit(dialogue_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(2000)
        dialogue_order += 1
    
    if dialogue_order == 8:
        pygame.draw.rect(screen, black, dialogueBoxOutline)
        pygame.draw.rect(screen, white, dialogueBox)
        dialogue_text = font.render("You used magic punch!", True, black)
        text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
        screen.blit(dialogue_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(2000)
        dialogue_order += 1

    if dialogue_order == 10:
        pygame.draw.rect(screen, black, dialogueBoxOutline)
        pygame.draw.rect(screen, white, dialogueBox)
        dialogue_text = font.render("You used heal hp!", True, black)
        text_rect = dialogue_text.get_rect(center=(dialogueBox.x + dialogueBox.width / 2, dialogueBox.y + dialogueBox.height / 2))
        screen.blit(dialogue_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(2000)
        dialogue_order += 1

mechanics.start_stopwatch()  
show_title_screen()
show_start_screen()
pygame.mixer.music.load("DQ Adventure Theme.mp3")
pygame.mixer.music.play(-1)

direction = None
moving = False
running = True
start = False
battle_screen_shown = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[K_a] and x > 0:
        x -= speed
        moving = True
        if direction != 'left':
            frame_count = 0
            direction = 'left'
    elif keys[K_d] and x < 600:
        x += speed
        moving = True
        if direction != 'right':
            frame_count = 0
            direction = 'right'
    elif keys[K_w] and y > 0:
        y -= speed
        moving = True
    elif keys[K_s] and y < 480:
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
        show_battle_screen()
        dx = 1000
        dy = 1000
        battle_screen_shown = False
        pygame.mixer.music.load("DQ Adventure Theme.mp3")
        pygame.mixer.music.play(-1)
        speed = 5

    pygame.display.flip()
    clock.tick(60)

pygame.quit()