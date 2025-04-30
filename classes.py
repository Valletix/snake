import pygame
from enum import Enum
import random

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(300, 300)
        self.last_move = None
        self.tail = []
    
    def draw(self, game_surface):
        player_rect = pygame.Rect(self.pos.x, self.pos.y, 30, 30)
        pygame.draw.rect(game_surface, "purple", rect=player_rect)


class PlayerTailPart:
    def __init__(self, predecessor, x, y):
        self.pos = pygame.Vector2(x, y)
        self.last_move = None
        self.predecessor = predecessor
    
    def move(self):
        if self.predecessor.last_move == "left":
            self.pos.x -= 30
        elif self.predecessor.last_move == "right":
            self.pos.x += 30
        elif self.predecessor.last_move == "up":
            self.pos.y -= 30
        elif self.predecessor.last_move == "down":
            self.pos.y += 30

    def set_last_move(self):
        self.last_move = self.predecessor.last_move
    
    def draw(self, game_surface):
        tail_rect = pygame.Rect(self.pos.x, self.pos.y, 30, 30)
        pygame.draw.rect(game_surface, "purple", rect=tail_rect)

class ScorePoint:
        def __init__(self, player):

            player_and_tail_positions = [player.pos]
            
            for tailpart in player.tail:
                player_and_tail_positions.append(tailpart.pos)

            possible_point_positions = []

            for i in range(0, 600, 30):
                for j in range(0, 600, 30):
                    point = pygame.Vector2(i, j)
                    if point not in player_and_tail_positions:
                        possible_point_positions.append(point)

            self.pos = random.choice(possible_point_positions)
            
            
        def draw(self, game_surface):
            point_rect = pygame.Rect(self.pos.x, self.pos.y, 30, 30)
            pygame.draw.rect(game_surface, "green", rect=point_rect)


class PlayerDirection(Enum):
    LEFT = (-30, 0)
    RIGHT = (30, 0)
    UP = (0, -30)
    DOWN = (0, 30)

