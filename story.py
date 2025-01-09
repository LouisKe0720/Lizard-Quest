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

x = 300
y = 220
dx = 500
dy = 220
speed = 5

pygame.init()

pygame.font.init()
font = pygame.font.SysFont('Arial', 16)

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


# Will use later, just keeping them here for now while I figure out the dialogue boxes

# mutants = [ImageSprite('MUTANT 1.png'), ImageSprite('MUTANT 2.png'), ImageSprite('MUTANT 3.png'), ImageSprite('MUTANT 4.png'),
#            ImageSprite('MUTANT 5.png'), ImageSprite('MUTANT 6.png'), ImageSprite('MUTANT 7.png')]

# mutant = random.choice(mutants)
# frame_1 = ImageSprite('PIXEL TEST F1.png')
# frame_2 = ImageSprite('PIXEL TEST F2.png')
# frame_3 = ImageSprite('PIXEL TEST F3.png')

# frames = [frame_1, frame_2, frame_3]

# frame_num = 0
# frame_count = 0
# frame_change = 5

# sprite = frame_1
# sprite_group = Group(sprite, mutant)

def black_fade():
    pygame.draw.rect(screen, black, (screen_width, screen_height))

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

battle_cg = pygame.image.load("STORY BATTLE CG.png")
spark_cg = pygame.image.load("STORY BATTLE SPARK CG.png")

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
scene = 0
dia = False
text = ""

battle_screen = pygame.image.load("BASE BATTLE SCREEN.png")
battle_screen = pygame.transform.scale(battle_screen, (screen_width, screen_height))

dialogue_box = pygame.image.load("DIALOGUE BOX 1.png")
dialogue_box = pygame.transform.scale(dialogue_box, (screen_width, screen_height))
dialogue_box2 = pygame.image.load("DIALOGUE BOX 2.png")
dialogue_box2 = pygame.transform.scale(dialogue_box2, (screen_width, screen_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)
    screen.blit(dialogue_box, (0,0))

    text = "*CRASH*"
    dialogue(text, 235, 400)
    
    if cg1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                show_cg(battle_cg)
                cg1_show = True
                text_num = 0
                texts = ["More Text", "Next Text", "And More Text"]
                
                while cg1_show and text_num < len(texts):
                    screen.blit(battle_cg, (0, 0))
                    screen.blit(dialogue_box, (0, 0))
                    dialogue(texts[text_num], 235, 400)
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

        if cg2 == True:
            screen.blits(spark_cg, (0,0))   
        
        pygame.display.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
