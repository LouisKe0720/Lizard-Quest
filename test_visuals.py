import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame.time import *
import random
import time

black = (0, 0, 0)
white = (255, 255, 255)
grass = (34, 139, 34)

x = 300
y = 220
dx = 500
dy = 220
speed = 2

pygame.init()
screen_width, screen_height = 600, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test Walking")
screen.fill(white)

clock = pygame.time.Clock()

class FallingPixel:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-40, screen_height)
        self.speed = random.randint(6,15)

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, black, (self.x, self.y, 20, 20))

def screen_cover(surface, cover_height):
    pygame.draw.rect(surface, (150, 150, 150), (0, -5, screen_width, cover_height+55))
    pygame.draw.rect(surface, (100, 100, 100), (0, -10, screen_width, cover_height+50))
    pygame.draw.rect(surface, (50, 50, 50), (0, -20, screen_width, cover_height+40))
    pygame.draw.rect(surface, black, (0, 0, screen_width, cover_height))

import pygame

def draw_grass(surface):
    pixel_spacing = 30
    for i in range(0, screen_width, pixel_spacing):
        for j in range(0, screen_height, pixel_spacing):
            pygame.draw.rect(surface, grass, (i, j, 3, 3))
            pygame.draw.rect(surface, grass, (i+5, j+6, 3, 3))
            pygame.draw.rect(surface, grass, (i-5, j+8, 3, 3))

def draw_block(surface, x, y, final_x, final_y):
    for i in range(x, final_x, pixel_spacing):
        for j in range(y, final_y, pixel_spacing):
            pygame.draw.rect(surface, (0, 0, 0), (i, j, 22, 22))
            pygame.draw.rect(surface, (50, 50, 50), (i, j, 20, 20))
            pygame.draw.rect(surface, (100, 100, 100), (i+2, j+2, 5, 8))

pixel_spacing = 30

def background(surface):
    pygame.draw.rect(surface, (105, 201, 97), (0, 0, screen_width, screen_height))
    draw_grass(screen)

    block_positions = [
        (540, 300, 540+90, screen_height), (450, 360, 450+90, screen_height), (390, 420, 390+90, screen_height), (0, 0, 90, 120), 
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

dracky = ImageSprite('Dracky_Artwork.png')
frame_1 = ImageSprite('PIXEL TEST F1.png')
frame_2 = ImageSprite('PIXEL TEST F2.png')
frame_3 = ImageSprite('PIXEL TEST F3.png')

frames = [frame_1, frame_2, frame_3]

frame_num = 0
frame_count = 0
frame_change = 5

sprite = frame_1
sprite_group = Group(sprite, dracky)

direction = None
moving = False
running = True
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
    elif keys[K_d] and x < 480:
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
    dracky.update(dx, dy)

    screen.fill(white)
    background(screen)
    sprite_group.draw(screen)
    
    if sprite.rect.colliderect(dracky.rect):
        speed = 0
        if pixel_falling:
            for pixel in falling_pixels:
                pixel.fall()
                pixel.draw(screen)
        if cover_height < screen_height:
                cover_height += 8
        if cover_height == screen_height:
                pixel_falling = False

        screen_cover(screen, cover_height)
    if pixel_falling == False:
        screen.fill(black)
        time.sleep(1)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
