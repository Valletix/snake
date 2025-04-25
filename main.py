import pygame
import os
from enum import Enum


os.environ["SDL_VIDEO_WINDOW_POS"] = "560,240" # Centers the Window for 1080p Screens

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

active_direction = PlayerDirection.RIGHT
timer = 0

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("orange")
    player_rect = pygame.Rect(player_pos.x, player_pos.y, 30, 30)
    pygame.draw.rect(screen, "purple", rect=player_rect)

    

    if active_direction == PlayerDirection.UP and timer == 10:
        if player_pos.y > 0:
            player_pos.y += active_direction.value[1]
            timer = 0
    elif active_direction == PlayerDirection.DOWN and timer == 10:
        if player_pos.y < 570:
            player_pos.y += active_direction.value[1]
            timer = 0
    elif active_direction == PlayerDirection.LEFT and timer == 10:
        if player_pos.x > 0:
            player_pos.x += active_direction.value[0]
            timer = 0
    elif active_direction == PlayerDirection.RIGHT and timer == 10:
        if player_pos.x < 570:
            player_pos.x += active_direction.value[0]
            timer = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if active_direction != PlayerDirection.DOWN:
            active_direction = PlayerDirection.UP
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if active_direction != PlayerDirection.UP:
            active_direction = PlayerDirection.DOWN
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if active_direction != PlayerDirection.RIGHT:
            active_direction = PlayerDirection.LEFT
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if active_direction != PlayerDirection.LEFT:
            active_direction = PlayerDirection.RIGHT
    

    pygame.display.flip()
    timer += 1

    clock.tick(60)
    

pygame.quit()