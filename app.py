import pygame
import random

pygame.init()

display_width = 600
display_height = 600

white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


character_center = pygame.image.load("flappy-bird(1).jpg")
character_center = pygame.transform.scale(character_center, (50, 35))

character = character_center

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (display_width, display_height))

logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (256, 68))

pipe_image = pygame.image.load("pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (250, 1750))

floor_image = pygame.image.load("floor.png")
floor_image = pygame.transform.scale(floor_image, (display_width, 46))

menu_image = pygame.image.load("menu.png")
menu_image = pygame.transform.scale(menu_image, (display_width - 200, display_height - 200))

button_normal = pygame.image.load("button(1).png")
button_normal = pygame.transform.scale(button_normal, (125, 75))
button_active = pygame.image.load("button(active).png")
button_active = pygame.transform.scale(button_active, (125, 75))
button_1 = button_normal
button_2 = button_normal

game_speed = 50

pipe_speed = 4

########################################################################################################################


def character_swap():
    global character
    if gravity > 45:
        angle = 45
    elif gravity < -15:
        angle = -15
    else:
        angle = gravity
    angle = 0 - angle

    character = rot_center(character_center, angle)


def write(text, font, size, colour, x, y):
    font_style = pygame.font.Font(font, size)
    message = font_style.render(text, True, colour)
    display.blit(message, [x, y])


def reset():
    global gravity, game_start, game_quit, game_menu, score, yval, floor1x, floor2x
    game_start = True
    game_quit = False
    game_menu = False
    gravity = 0
    yval = display_height / 2
    score = 0
    floor1x = 0
    floor2x = display_width


def game():
    global gravity, game_start, game_quit, game_menu, score, yval, floor1x, floor2x, button_1, button_2

    pipes = [[display_width, (random.randint(150, int(display_height - 250))) - 900]]

    while game_start and not game_quit and not game_menu:
        gravity = 0
        yval = display_height / 2

        display.blit(background_image, [0, 0])

        write("Press space to start", "FlappyBirdy.ttf", 60, white, 145, 350)
        display.blit(logo, [180, 200])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_start = False
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_quit = False
                    game_start = False

        pygame.display.update()

        clock.tick(game_speed)

    while game_menu and not game_start and not game_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_menu = False
                game_start = False
                game_quit = True
                game()

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if 275 > x > 150 and 450 > y > 375:
                    reset()
                    game()
                if 460 > x > 335 and 450 > y > 375:
                    game_quit = True
                    game_menu = False
                    game_start = False
                    game()

        x, y = pygame.mouse.get_pos()
        if 275 > x > 150 and 450 > y > 375:
            button_1 = button_active
        else:
            button_1 = button_normal
        if 460 > x > 335 and 450 > y > 375:
            button_2 = button_active
        else:
            button_2 = button_normal

        display.blit(menu_image, (100, 100))
        display.blit(button_1, (150, 375))
        display.blit(button_2, (335, 375))

        write("You Lost", "FlappyBirdy.ttf", 100, white, 190, 170)
        write(str(score), "DisposableDroidBB.ttf", 100, white, 275, 250)

        write("Play", "DisposableDroidBB.ttf", 50, white, 170, 385)
        write("Quit", "DisposableDroidBB.ttf", 50, white, 355, 385)

        pygame.display.update()
        clock.tick(game_speed)

    while not game_quit and not game_start and not game_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
                game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or pygame.K_UP:
                    gravity = -7
                    character_swap()

        yval += gravity

        if (int(yval/4)) == yval/4:
            gravity += 1

        if 10 > gravity > 0:
            character_swap()
        if 10 < gravity:
            character_swap()

        display.blit(background_image, [0, 0])
        display.blit(character, [100, int(yval)])

        for pipe in pipes:
            pipe[0] -= pipe_speed
            display.blit(pipe_image, (pipe[0], pipe[1]))

            if pipe[0] == 200:
                pipes.append([display_width, (random.randint(150, int(display_height - 250))) - 900])

            if pipe[0] == 0:
                score += 1

            # pygame.draw.rect(display, red, [pipe[0] + 7, pipe[1] + 1005, 130, 810], 2)

            if yval < pipe[1] + 810 and 5 < pipe[0] < 135:
                game_start = False
                game_quit = False
                game_menu = True
                game()

            if yval > pipe[1] + 1005 and 5 < pipe[0] < 135:
                game_start = False
                game_quit = False
                game_menu = True
                game()

        if pipes[0][0] < -200:
            del pipes[0]

        if floor1x > 0 - display_width:
            floor1x -= pipe_speed
        if floor2x > 0 - display_width:
            floor2x -= pipe_speed
        if floor2x == 0:
            floor1x = floor2x + display_width
        if floor1x == 0:
            floor2x = floor1x + display_width

        display.blit(floor_image, (floor1x, display_height-46))
        display.blit(floor_image, (floor2x, display_height-46))

        write(str(score), "DisposableDroidBB.ttf", 100, white, 250, 30)

        pygame.display.update()

        if yval < 0:
            game_start = False
            game_quit = False
            game_menu = True
            game()
        if (yval + 35) > display_height - 46:
            game_start = False
            game_quit = False
            game_menu = True
            game()

        clock.tick(game_speed)

    if game_quit:
        pygame.quit()
        quit()


reset()
game()
