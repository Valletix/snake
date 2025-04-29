import pygame
from enum import Enum
import random


def start_screen(screen):
    clock = pygame.time.Clock()
    pygame.font.init()
    text = pygame.font.Font(None, 30)
    image = text.render("Hello Mr. Snek! Press Space to play!",
                 1, "black")
    start_screen = True
    
    while start_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False

        screen.fill("orange")


        screen.blit(image, (120,270))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_screen = False
            gameplay_loop(screen)

        pygame.display.flip()

        clock.tick(60)


def game_over_screen(screen):

    pygame.mixer.music.stop()
    clock = pygame.time.Clock()
    pygame.font.init()
    text = pygame.font.Font(None, 30)
    image = text.render("Game Over! Press Enter to go to the Titlescreen",
                 1, "black")
    game_over_screen = True
    
    while game_over_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_screen = False

        screen.fill("orange")


        screen.blit(image, (70,270))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over_screen = False
            start_screen(screen)

        pygame.display.flip()

        clock.tick(60)
        

    

def gameplay_loop(screen):

    pygame.mixer.init()
    pygame.mixer.music.load("soundfiles/RICARDO.mp3")
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    game_loop = True


    class Player:
        def __init__(self):
            self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)
            self.last_move = None
            self.tail = []

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
        
        def draw(self):
            tail_rect = pygame.Rect(self.pos.x, self.pos.y, 30, 30)
            pygame.draw.rect(screen, "purple", rect=tail_rect)

    def move_tailparts_and_set_last_moves(tailparts):
        for tailpart in tailparts[::-1]:
            tailpart.move()
            tailpart.last_move = tailpart.predecessor.last_move

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

        
    
    player = Player()
    active_direction = PlayerDirection.RIGHT
    movement_timer = 0
    movement_cooldown = 8
    active_point = None

    while game_loop:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        screen.fill("orange")

        if active_point == None:
            active_point = ScorePoint()
        
        active_point.draw_point()

        player_rect = pygame.Rect(player.pos.x, player.pos.y, 30, 30)
        pygame.draw.rect(screen, "purple", rect=player_rect)
        for tailpart in player.tail:
            tailpart.draw()

        if active_direction == PlayerDirection.UP and movement_timer == 8:
            if player.pos.y > 0:
                player.pos.y += active_direction.value[1]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "up"
                
            else:
                game_loop = False
                game_over_screen(screen)
                
        elif active_direction == PlayerDirection.DOWN and movement_timer == 8:
            if player.pos.y < 570:
                player.pos.y += active_direction.value[1]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "down"
            else:
                game_loop = False
                game_over_screen(screen)
                
        elif active_direction == PlayerDirection.LEFT and movement_timer == 8:
            if player.pos.x > 0:
                player.pos.x += active_direction.value[0]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "left"
            else:
                game_loop = False
                game_over_screen(screen)
                
        elif active_direction == PlayerDirection.RIGHT and movement_timer == 8:
            if player.pos.x < 570:
                player.pos.x += active_direction.value[0]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "right"
            else:
                game_loop = False
                game_over_screen(screen)
        
        for tailpart in player.tail:
            if tailpart.pos == player.pos:
                game_loop = False
                game_over_screen(screen)

        if player.pos == active_point.point_pos:
            active_point = None
            
            if len(player.tail) == 0:
                predecessor =  player
            else:
                predecessor = player.tail[-1]
            
            if predecessor.last_move == "left":
                new_part = PlayerTailPart(predecessor, predecessor.pos.x + 30, predecessor.pos.y)
            elif predecessor.last_move == "right":
                new_part = PlayerTailPart(predecessor, predecessor.pos.x - 30, predecessor.pos.y)
            elif predecessor.last_move == "up":
                new_part = PlayerTailPart(predecessor, predecessor.pos.x, predecessor.pos.y + 30)
            elif predecessor.last_move == "down":
                new_part = PlayerTailPart(predecessor, predecessor.pos.x, predecessor.pos.y - 30)
            
            player.tail.append(new_part)


        
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

    
