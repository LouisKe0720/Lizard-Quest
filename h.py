import pygame
from pygame.locals import *
from pygame.sprite import *
import random
import time
import mechanics

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
grass = (34, 139, 34)

# Screen settings
screen_width, screen_height = 600, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load('LQ LOGO.png'))
pygame.display.set_caption("Test Walking")
screen.fill(white)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

# Load images
p_block = pygame.image.load("PURPLE BLOCK TEXTURE.png")
p_block = pygame.transform.scale(p_block, (22, 22))
p_region = pygame.image.load("PURPLE REGION TEXTURE.png")
p_water = pygame.image.load("WATER TEXTURE.png")

# Load music
pygame.mixer.music.load("DQ Overture XI.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Define buttons
start_button = pygame.Rect(20, 170, 400, 75)
time_button = pygame.Rect(20, 370, 400, 75)
back_button = pygame.Rect(300, 370, 100, 75)
skill_button = pygame.Rect(5, 285, 110, 40)
items_button = pygame.Rect(5, 315, 110, 40)
flee_button = pygame.Rect(5, 373, 110, 40)

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

# Define classes
class FallingPixel:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-40, screen_height)
        self.speed = random.randint(6, 15)

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, black, (self.x, self.y, 20, 20))

class ImageSprite(Sprite):
    def __init__(self, filename):
        Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, x, y):
        self.rect.center = (x, y)

# Define functions
def draw_grass(surface, pixel_spacing):
    for i in range(0, screen_width, pixel_spacing):
        for j in range(0, screen_height, pixel_spacing):
            surface.blit(p_region, (i, j))

def draw_block(surface, x, y, final_x, final_y, pixel_spacing=20):
    for i in range(x, final_x, pixel_spacing):
        for j in range(y, final_y, pixel_spacing):
            surface.blit(p_block, (i, j))

def background(surface):
    pygame.draw.rect(surface, (105, 201, 97), (0, 0, screen_width, screen_height))
    draw_grass(screen, 15)
    block_positions = [
        (540, 300, 540 + 90, screen_height), (450, 360, 450 + 90, screen_height), (390, 420, 390 + 90, screen_height), (0, 0, 90, 120),
        (0, 0, 45, 200), (0, 0, 20, 300)
    ]
    for x, y, final_x, final_y in block_positions:
        draw_block(screen, x, y, final_x, final_y)

def screen_cover(surface, cover_height):
    pygame.draw.rect(surface, (150, 150, 150), (0, -5, screen_width, cover_height + 55))
    pygame.draw.rect(surface, (100, 100, 100), (0, -10, screen_width, cover_height + 50))
    pygame.draw.rect(surface, (50, 50, 50), (0, -20, screen_width, cover_height + 40))
    pygame.draw.rect(surface, black, (0, 0, screen_width, cover_height))

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
    while waiting:
        pygame.draw.rect(screen, white, start_button)
        pygame.draw.rect(screen, white, time_button)
        screen.blit(start_image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False
                elif time_button.collidepoint(event.pos):
                    show_time_screen()

def show_time_screen():
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
        screen.fill(white)
        rendered_text = font.render(time_text, True, black)
        screen.blit(rendered_text, (screen_width / 2 - 150, screen_height / 2 - 50))
        pygame.draw.rect(screen, black, back_button)
        pygame.display.flip()
        clock.tick(60)

def show_battle_screen():
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
                    show_flee_screen()
        screen.blit(battle_screen, (0, 0))
        draw_buttons()
        pygame.display.update()

def draw_buttons():
    pygame.draw.rect(screen, white, skill_button)
    pygame.draw.rect(screen, white, items_button)
    pygame.draw.rect(screen, white, flee_button)

def show_skills_screen():
    skills_opened = True
    while skills_opened:
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

def show_flee_screen():
    flee_opened = True
    while flee_opened:
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

# Main game loop
mechanics.start_stopwatch()
show_title_screen()
show_start_screen()
pygame.mixer.music.load("DQ Adventure Theme.mp3")
pygame.mixer.music.play(-1)

x, y = 300, 220
dx, dy = 500, 220
speed = 5
direction = None
moving = False
running = True
battle_screen_shown = False
pixel_falling = True
cover_height = 0
num_pixels = 37
falling_pixels = [FallingPixel() for _ in range(num_pixels)]

mutants = [ImageSprite(f'MUTANT {i}.png') for i in range(1, 8)]
mutant = random.choice(mutants)
frames = [ImageSprite(f'PIXEL TEST F{i}.png') for i in range(1, 4)]
frame_num = 0
frame_count = 0
frame_change = 5
sprite = frames[0]
sprite_group = Group(sprite, mutant)

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
            if direction == 'left' and frame_num != 0:
                sprite.image = pygame.transform.flip(sprite.image, True, False)

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
    
    if not pixel_falling and battle_screen_shown:
        show_battle_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()