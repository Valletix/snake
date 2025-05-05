import pygame
import os
from game_functions import start_screen, random_input


os.environ["SDL_VIDEO_WINDOW_POS"] = "560,190" # Centers the Window for 1080p Screens


pygame.init()
flags = pygame.SCALED | pygame.RESIZABLE
pygame.display.set_caption("Mr. Snek")
display = pygame.display.set_mode((800,700), flags)

game_surface = pygame.Surface((600,600), flags)

#random_input(display, game_surface)
start_screen(display, game_surface)

pygame.quit()

