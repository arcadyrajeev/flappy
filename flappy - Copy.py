import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 600))
    screen.blit(floor_surface, (floor_x_pos + 576, 600))

def draw_bg():
    screen.blit(bg_surface_day, (bg_x_pos, 0))
    screen.blit(bg_surface_day, (bg_x_pos + 700, 0))

    if score >= 5:
        screen.blit(bg_surface_ev, (bg_x_pos, 0))
        screen.blit(bg_surface_ev, (bg_x_pos + 700, 0))

    if score >= 20:
        screen.blit(bg_surface_gn, (bg_x_pos, 0))
        screen.blit(bg_surface_gn, (bg_x_pos + 700, 0))



def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(1000, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(1000, random_pipe_pos - random.choice(pipe_gap)))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def delete_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx <= -100:
            pipe_array.pop(0)


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 900:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotate(bird, -bird_movement*3)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(350, 100))
        screen.blit(score_surface, score_rect)

    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score  {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(350, 250))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Highscore  {str(int(highscore))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(350, 320))
        screen.blit(high_score_surface, high_score_rect)



def increase_score(pipes):
    for pipe in pipes:
        if pipe.centerx == 75:
            return True


def update_high_score(score, highscore):
    if score > highscore:
        highscore = score

        f = open('data/highscore.txt', 'w')
        f.write(str(highscore))
        f.close()
    return highscore


pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Flappy by RKD")
clock = pygame.time.Clock()


# game variables
gravity = 0.15
bird_movement = 0
game_active = False
menu = True
score = 0

game_font = pygame.font.SysFont('Showcard Gothic', 40)
game_font2 = pygame.font.SysFont('Showcard Gothic', 70)


bg_surface_day =pygame.image.load('resources/images/background.png').convert()
bg_surface_ev =pygame.image.load('resources/images/background2.png').convert()
bg_surface_gn =pygame.image.load('resources/images/background3.png').convert()

bg_x_pos = 0


floor_surface = pygame.image.load('resources/images/base2.png').convert()
floor_x_pos = 0


bird_down = pygame.image.load('resources/images/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('resources/images/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('resources/images/yellowbird-upflap.png').convert_alpha()
bird_red = pygame.image.load('resources/images/redbird-midflap.png').convert_alpha()
bird_frames = [bird_down, bird_mid, bird_up, bird_red]
bird_index = 1
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 350))

BIRDFLAP = pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP, 100)


pipe_surface = pygame.transform.scale2x(pygame.image.load('resources/images/pipe-green.png').convert())

pipe_array = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

pipe_height = [300, 350, 300, 380, 400, 420,  450]
pipe_gap =[180, 200, 220, 240, 280]
p = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


game_over_surface = pygame.image.load('resources/images/message20.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(350, 350))

crash_surface = pygame.image.load('resources/images/crash.png').convert_alpha()

black_surface = pygame.transform.scale2x(pygame.image.load('resources/images/black2.png').convert_alpha())
black_rect = black_surface.get_rect(center=(350, 288))

menu_surface = pygame.image.load('resources/images/menu2.png').convert_alpha()
menu_rect = menu_surface.get_rect(center=(350, 350))

esc_surface =pygame.image.load('resources/images/message3.png').convert_alpha()
esc_rect = esc_surface.get_rect(center=(350, 500))


# sound
flap_sound = pygame.mixer.Sound('resources/Sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('resources/Sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('resources/Sound/sfx_point.wav')

# data
f = open('data/highscore.txt', 'r')
highscore = int(f.read())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active is True:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()

            if event.key == pygame.K_SPACE and menu is True:
                game_active = True
                menu = False

            if event.key == pygame.K_RETURN and game_active is False:
                game_active = True
                score = 0
                bird_movement = 0
                pipe_array.clear()
                bird_rect.center = (100, 350)

            if event.key == pygame.K_BACKSPACE and game_active is False:
                menu = True
                score = 0
                bird_movement = 0
                pipe_array.clear()
                bird_rect.center = (100, 350)

            if event.key == pygame.K_ESCAPE and menu:
                pygame.quit()
                sys.exit()


        if event.type == SPAWNPIPE and not menu and game_active:
            pipe_array.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    if game_active:
        bg_x_pos -= 1

        draw_bg()
        if bg_x_pos <= -700:
            bg_x_pos = 0



    # screen.blit(bg_surface, (0, 0))

    if menu:

        bg_x_pos -= 1

        draw_bg()
        if bg_x_pos <= -700:
            bg_x_pos = 0

        # bird
        bird_movement += 3
        bird_movement -= 3
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        floor_x_pos -= 5
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

        screen.blit(menu_surface, menu_rect)



    elif game_active and not menu :
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_array)

        # pipes
        pipe_array = move_pipes(pipe_array)
        draw_pipes(pipe_array)
        score_display('main_game')

        if increase_score(pipe_array):
            score += 1
            score_sound.play()
        delete_pipes(pipe_array)

        # floor
        floor_x_pos -= 5
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

    elif game_active is False and menu is False:
        draw_bg()
        draw_pipes(pipe_array)
        draw_floor()

        bird_index = 3
        bird_surface, bird_rect = bird_animation()
        screen.blit(bird_surface, bird_rect)
        crash_rect = crash_surface.get_rect(center=(100, bird_rect.centery - 100))
        screen.blit(crash_surface, crash_rect)

        screen.blit(black_surface, black_rect)
        screen.blit(game_over_surface, game_over_rect)
        highscore = update_high_score(score,highscore)
        score_display('game_over' )


    clock.tick(120)
    pygame.display.update()