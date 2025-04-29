import pygame
import os
from game_functions import start_screen


os.environ["SDL_VIDEO_WINDOW_POS"] = "660,240" # Centers the Window for 1080p Screens


pygame.init()
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((600,600), flags)


start_screen(screen)

pygame.quit()
