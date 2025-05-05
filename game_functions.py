import pygame
from classes import Player, PlayerDirection, PlayerTailPart, ScorePoint
from constants import FONT


def random_input(display, game_surface):

    clock = pygame.time.Clock()
    input_box = pygame.Rect(150, 150, 250, 50)
    text = ""


    random_screen = True

    while random_screen:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                random_screen = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 10:
                        text += event.unicode

        

        display.fill("orange")
        pygame.draw.rect(display, "black", pygame.Rect(99, 49, 602, 602), width=2)

        game_surface.fill("orange")

        txt_surface = FONT.render(text, True, "black")

        pygame.draw.rect(game_surface, "black", input_box, 2)

        game_surface.blit(txt_surface, (input_box.x+5, input_box.y+5))

        display.blit(game_surface, (100, 50))
        

        
        



        pygame.display.flip()

        clock.tick(60)



def start_screen(display, game_surface):
    clock = pygame.time.Clock()

    surface_hello = FONT.render("Hello Mr. Snek!", 1, "black")
    surface_button = FONT.render("Press Space to play!", 1, "black")
    size_hello = FONT.size("Hello Mr. Snek!")
    size_button = FONT.size("Press Space to play!")
    start_screen = True
    
    while start_screen:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
        
        display.fill("orange")
        pygame.draw.rect(display, "black", pygame.Rect(99, 49, 602, 602), width=2)

        display.blit(game_surface, (100, 50))

        game_surface.fill("orange")


        game_surface.blit(surface_hello, ((game_surface.get_width() - size_hello[0]) / 2 ,
                                    (game_surface.get_height() - size_hello[1])/ 2 - 20))
        game_surface.blit(surface_button, ((game_surface.get_width() - size_button[0])/ 2 ,
                                     (game_surface.get_height() - size_button[1])/ 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_screen = False
            gameplay_loop(display, game_surface)

        pygame.display.flip()

        clock.tick(60)


def game_over_screen(display, game_surface):

    pygame.mixer.music.stop()
    clock = pygame.time.Clock()
    pygame.font.init()

    surface_game_over = FONT.render("Game Over!", 1, "black")
    surface_button = FONT.render("Press Enter to go", 1, "black")
    surface_titlescreen = FONT.render("to the Titlescreen.", 1, "black")
    size_game_over = FONT.size("Game Over!")
    size_button = FONT.size("Press Enter to go")
    size_titlescreen = FONT.size("to the Titlescreen.")

    game_over_screen = True
    
    while game_over_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_screen = False

        pygame.draw.rect(display, "black", pygame.Rect(99, 49, 602, 602), width=2)
        display.blit(game_surface, (100, 50))

        game_surface.fill("orange")


        game_surface.blit(surface_game_over, ((game_surface.get_width() - size_game_over[0]) / 2 ,
                                    (game_surface.get_height() - size_game_over[1])/ 2 - 20))
        game_surface.blit(surface_button, ((game_surface.get_width() - size_button[0])/ 2 ,
                                     (game_surface.get_height() - size_button[1])/ 2 + 20))
        game_surface.blit(surface_titlescreen, ((game_surface.get_width() - size_titlescreen[0])/ 2 ,
                                     (game_surface.get_height() - size_titlescreen[1])/ 2 + 45))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over_screen = False
            start_screen(display, game_surface)

        pygame.display.flip()

        clock.tick(60)
    


def draw_score(display, score):

    surface_score = FONT.render(f"{score}", 1, "black")
    display.blit(surface_score, (100, 10))

def gameplay_loop(display, game_surface):

    pygame.mixer.init()
    pygame.mixer.music.load("ressources/soundfiles/RICARDO.mp3")
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    game_loop = True
    
    def move_tailparts_and_set_last_moves(tailparts):
        for tailpart in tailparts[::-1]:
            tailpart.move()
            tailpart.last_move = tailpart.predecessor.last_move
        
    current_score = 0
    player = Player()
    active_direction = PlayerDirection.RIGHT
    movement_timer = 0
    movement_cooldown = 8
    active_score_point = None


    while game_loop:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        display.fill("orange")
        pygame.draw.rect(display, "black", pygame.Rect(99, 49, 602, 602), width=2)

        display.blit(game_surface, (100, 50))

        game_surface.fill("orange")

        draw_score(display, current_score)

        if active_score_point == None:
            active_score_point = ScorePoint(player)

        player.draw(game_surface)
        active_score_point.draw(game_surface)
        for tailpart in player.tail:
            tailpart.draw(game_surface)

        if active_direction == PlayerDirection.UP and movement_timer == 8:
            if player.pos.y > 0:
                player.pos.y += active_direction.value[1]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "up"
                
            else:
                game_loop = False
                game_over_screen(display, game_surface)
                
        elif active_direction == PlayerDirection.DOWN and movement_timer == 8:
            if player.pos.y < 570:
                player.pos.y += active_direction.value[1]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "down"
            else:
                game_loop = False
                game_over_screen(display, game_surface)
                
        elif active_direction == PlayerDirection.LEFT and movement_timer == 8:
            if player.pos.x > 0:
                player.pos.x += active_direction.value[0]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "left"
            else:
                game_loop = False
                game_over_screen(display, game_surface)
                
        elif active_direction == PlayerDirection.RIGHT and movement_timer == 8:
            if player.pos.x < 570:
                player.pos.x += active_direction.value[0]
                if len(player.tail) > 0:
                    move_tailparts_and_set_last_moves(player.tail)
                player.last_move = "right"
            else:
                game_loop = False
                game_over_screen(display, game_surface)
        
        for tailpart in player.tail:
            if tailpart.pos == player.pos:
                game_loop = False
                game_over_screen(display, game_surface)

        if player.pos == active_score_point.pos:
            active_score_point = None
            
            current_score += 10

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

    
