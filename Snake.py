import pygame
import time
import random

pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKRED = (155, 0, 0)

WIDTH = 800
HEIGHT = 800
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PogChamp")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 32)


def snake(block_size, snake_list):
    for XnY in snake_list:
        pygame.draw.rect(screen, BLACK, [XnY[0], XnY[1], block_size, block_size])
        pygame.draw.rect(screen, WHITE, [XnY[0] + 1, XnY[1] + 1, block_size - 2, block_size - 2])


def message_to_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])
    pygame.display.update()


# sprite group
all_sprites = pygame.sprite.Group()

start = time.time()


def start_menu():
    screen.fill(BLACK)
    message_to_screen("PRESS \"SPACE\" TO START GAME", WHITE, int(WIDTH * 0.3), int(HEIGHT / 2))
    start_press = True
    while start_press:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_press = False


def gameloop():
    # Snake
    lead_x = 400
    lead_y = 400
    lead_changex = 0
    lead_changey = 0
    block_size = 20
    snake_list = []
    snake_length = 1
    apple_width = 20
    direction = ""

    # Apple
    apple_x = random.randrange(0, WIDTH - apple_width, 20)
    apple_y = random.randrange(0, HEIGHT - apple_width, 20)

    game_over = False
    running = True
    while running:
        while game_over:  # while
            screen.fill(BLACK)
            message_to_screen("YOU DIED! PRESS \"R\" TO RESTART OR \"Q\" TO QUIT", RED, int(WIDTH * 0.175),
                              int(HEIGHT * 0.5))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # if "q" close game
                        running = False
                        game_over = False
                    if event.key == pygame.K_r:  # if "r" reset game
                        gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    lead_changex = - block_size
                    lead_changey = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    lead_changex = block_size
                    lead_changey = 0
                    direction = "right"
                elif event.key == pygame.K_UP and direction != "down":
                    lead_changex = 0
                    lead_changey = - block_size
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    lead_changex = 0
                    lead_changey = block_size
                    direction = "down"

        lead_x += lead_changex
        lead_y += lead_changey
        # PROCESS INPUT
        # collision on border
        if lead_x >= WIDTH or lead_x < 0 or lead_y >= HEIGHT or lead_y < 0:
            game_over = True

        # UPDATE
        # if snake eats apple
        if lead_x + block_size > apple_x and lead_x < apple_x + apple_width and \
                lead_y + block_size > apple_y and lead_y < apple_y + apple_width:
            apple_x = random.randrange(0, WIDTH - block_size, 20)
            apple_y = random.randrange(0, HEIGHT - block_size, 20)
            snake_length += 1

        # RENDER
        # fill screen with black before drawing
        screen.fill(BLACK)
        # game score
        message_to_screen("Score: " + str(snake_length - 1), WHITE, 10, 10)
        # apple
        pygame.draw.rect(screen, BLACK, [apple_x, apple_y, apple_width, apple_width])
        pygame.draw.rect(screen, DARKRED, [apple_x + 1, apple_y + 1, apple_width - 2, apple_width - 2])
        # snake
        snake_head = [lead_x, lead_y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for eachSegment in snake_list[:-1]:
            if eachSegment == snake_head:
                game_over = True

        snake(block_size, snake_list)
        pygame.display.update()
        clock.tick(FPS)


start_menu()
gameloop()
screen.fill(BLACK)
message_to_screen("BYE!  =)", WHITE, int(WIDTH * 0.45), int(HEIGHT * 0.5))
time.sleep(2)
pygame.quit()
quit()
