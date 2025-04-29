import pygame
import os
from enum import Enum
import random


os.environ["SDL_VIDEO_WINDOW_POS"] = "660,240" # Centers the Window for 1080p Screens

pygame.mixer.init()
pygame.mixer.music.load("soundfiles/RICARDO.mp3")
pygame.mixer.music.play()
pygame.init()
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((600,600), flags)
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)


class PlayerDirection(Enum):
    LEFT = (-30, 0)
    RIGHT = (30, 0)
    UP = (0, -30)
    DOWN = (0, 30)

class ScorePoint:
    def __init__(self):
        self.point_pos = pygame.Vector2(random.randrange(0, 600, 30), random.randrange(0, 600, 30))
        
    
    def draw_point(self):
        point_rect = pygame.Rect(self.point_pos.x, self.point_pos.y, 30, 30)
        pygame.draw.rect(screen, "green", rect=point_rect)

    

active_direction = PlayerDirection.RIGHT
movement_timer = 0
movement_cooldown = 8
active_point = None

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill("orange")

    if active_point == None:
        active_point = ScorePoint()
    
    active_point.draw_point()

    player_rect = pygame.Rect(player_pos.x, player_pos.y, 30, 30)
    pygame.draw.rect(screen, "purple", rect=player_rect)

   

    

    if active_direction == PlayerDirection.UP and movement_timer == 8:
        if player_pos.y > 0:
            player_pos.y += active_direction.value[1]
            
    elif active_direction == PlayerDirection.DOWN and movement_timer == 8:
        if player_pos.y < 570:
            player_pos.y += active_direction.value[1]
            
    elif active_direction == PlayerDirection.LEFT and movement_timer == 8:
        if player_pos.x > 0:
            player_pos.x += active_direction.value[0]
            
    elif active_direction == PlayerDirection.RIGHT and movement_timer == 8:
        if player_pos.x < 570:
            player_pos.x += active_direction.value[0]
    
    if player_pos == active_point.point_pos:
        active_point = None
    
    if movement_timer == 8:
        movement_timer = 0
        movement_cooldown = 8
    
    movement_timer += 1
    movement_cooldown += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if active_direction != PlayerDirection.DOWN and movement_cooldown > 8:
            active_direction = PlayerDirection.UP
            movement_cooldown = 0
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if active_direction != PlayerDirection.UP and movement_cooldown > 8:
            active_direction = PlayerDirection.DOWN
            movement_cooldown = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if active_direction != PlayerDirection.RIGHT and movement_cooldown > 8:
            active_direction = PlayerDirection.LEFT
            movement_cooldown = 0
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if active_direction != PlayerDirection.LEFT and movement_cooldown > 8:
            active_direction = PlayerDirection.RIGHT
            movement_cooldown = 0
    

    pygame.display.flip()

    clock.tick(60)
    

pygame.quit()