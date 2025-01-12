import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame.time import *
import random
import time
import mechanics

black = (0, 0, 0)
white = (255, 255, 255)
grass = (34, 139, 34)

x = 200
y = 380
dx = 400
dy = 380
speed = 5

pygame.init()

pygame.font.init()
font = pygame.font.SysFont('Arial', 17)

screen_width, screen_height = 600, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load('LQ LOGO.png'))
pygame.display.set_caption("Test Walking")
screen.fill(white)

clock = pygame.time.Clock()

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

frame_1gn = ImageSprite('NO GUN 1.png')
frame_2gn = ImageSprite('NO GUN 2.png')
frame_3gn = ImageSprite('NO GUN 3.png')

frames = [frame_1, frame_2, frame_3]
framesgn = [frame_1gn, frame_2gn, frame_3gn]

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
    screen.blit(start_image, (0, 0))
    pygame.display.flip()

    waiting = True
    start_button = pygame.Rect(20, 170, 400, 75)
    time_button = pygame.Rect(20, 370, 400, 75)
    back_button = pygame.Rect(300, 370, 100, 75)
    
    while waiting:
        pygame.draw.rect(screen, (255, 255, 255), start_button)
        pygame.draw.rect(screen, (255, 255, 255), time_button)
        screen.blit(start_image, (0, 0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    fade_surface = pygame.Surface((screen_width, screen_height))
                    fade_surface.fill(black)
                    alpha = 0
                    fade_duration = 60
                    while alpha < 255:
                        screen.blit(start_image, (0, 0))
                        fade_surface.set_alpha(alpha)
                        screen.blit(fade_surface, (0, 0))
                        pygame.display.flip()
                        alpha += 255 // fade_duration
                        clock.tick(60)
                    
                    waiting = False
                elif time_button.collidepoint(event.pos):  # Time Screen
                    time_waiting = True
                    while time_waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if back_button.collidepoint(event.pos):
                                    time_waiting = False

                        time_text = mechanics.time_elapsed()
                        screen.fill(white)  # Fill the screen with white color
                        rendered_text = font.render(time_text, True, black)  # Render the time text
                        screen.blit(rendered_text, (screen_width/2 - 150, screen_height/2 - 50))  # Display the rendered text
                        pygame.draw.rect(screen, (0,0,0), back_button)
                        pygame.display.flip()
                        clock.tick(60)                 

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

battle_cg = pygame.transform.scale(pygame.image.load("STORY BATTLE CG.png"), (screen_width, screen_height))
spark_cg = pygame.transform.scale(pygame.image.load("STORY BATTLE SPARK CG.png"), (screen_width, screen_height))
cave_bg = pygame.image.load("CAVE BG.png")

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
    rendered_text = font.render(text, True, white)
    screen.blit(rendered_text, (text_x, text_y))

mechanics.start_stopwatch()
show_title_screen()
show_start_screen()
time.sleep(2)
show_dialogue_box()

direction = None
moving = False
running = True
start = False
cg1 = True
cg1_show = False
cg2 = False
cg2_show = False
text = ""
first_s = True
sec_s = False
cave_cg = False

battle_screen = pygame.image.load("BASE BATTLE SCREEN.png")
battle_screen = pygame.transform.scale(battle_screen, (screen_width, screen_height))

dialogue_box = pygame.image.load("DIALOGUE BOX 1.png")
dialogue_box = pygame.transform.scale(dialogue_box, (screen_width, screen_height))

black_bg = pygame.image.load("BLACK BG.png")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)

    while first_s == True:
        screen.blit(black_bg, (0,0))
        screen.blit(dialogue_box, (0,0))
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
        texts = ["Lizard 1: The mutant king shot THE orb?!", "Lizard 2: WHAT!? OUR KING IS BARELY HOLDIN’ UP!", "*BANG*",
                         "Lizard King: AHHH!!!!!", "MC lizard: FATHER!", "Lizard 1: THEY GOT THE KING!", "Mutant: KNEEL BEFORE OUR KING’S POWER!",
                         "Lizard King: …Hey kiddo.", "MC: DON’T TALK!! I’LL GET SUPPLIES TO STOP THE BLEEDING!", 
                         "Lizard King: You may not understand what I’m about to say to you but…","Lizard King: …When the time comes…",
                         "Lizard King: Avenge for us ol’ lizards, ok?", "MC: STOP TALKING AS IF YOU’RE GOING TO DIE!", "Lizard King: …Keep yourself alive until then, little guy.",
                         "Lizard King: That weird-lookin’ matter won’t keep itself from you.","Lizard King: …", "Lizard King: I think…", "Mutant: I SAID KNEEL BEFORE THE KING’S POWER!",
                         "Lizard King: …you may just be the one to succee.…"]
        texts_x = [150, 100, 260, 230, 225, 195, 120, 210, 42, 26, 170, 150, 110, 105, 70, 240, 220, 100, 120]
                
        while cg1_show and text_num < len(texts):
                    screen.blit(battle_cg, (0, 0))
                    screen.blit(dialogue_box, (0, 0))
                    dialogue(texts[text_num], texts_x[text_num], 402)
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
                                show_cg(spark_cg)
                                cg2_show = True
                                sec_s = True
                                text2_num = 0
        
    if cg2 == True:
            if sec_s == True:
                screen.blit(spark_cg, (0, 0))
                screen.blit(dialogue_box, (0, 0))
                dialogue("*BANG*", 240, 400)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    sec_s = False
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
                                if text2_num >= len(texts):
                                    cg2_show = False
                                    cg2 = False
                        
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
    elif keys[K_w] and y > 380:
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
    screen.blit(cave_bg, (0,0))
    sprite_group.draw(screen)

    pygame.display.update()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
