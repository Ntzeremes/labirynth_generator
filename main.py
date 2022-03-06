import pygame
from algorithm import *
from start_gui import starting_gui

pygame.init()


def create_grid(screen, screen_width,screen_height, width, height, pad):
    """ Creates the height x width  grid of the labyrinth.
    Used when we start the program and every time we reset the labyrinth"""
    screen.fill((80, 80, 80))
    block = screen_width // width
    pygame.draw.line(screen, (0, 0, 0), (0, pad), (screen_width, pad))
    for i in range(height - 1):
        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1) * block + pad), (screen_width, (i + 1) * block + pad))
    for j in range(width):
        pygame.draw.line(screen, (0, 0, 0), ((j + 1) * block, pad), ((j + 1) * block, screen_height + pad))


def main(width, height):
    """Initializes and visualizes the labyrinth using pygame and the classes from algorithm.py.
    """

    # pygame
    top_pad = 50
    right_pad = 100
    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode((screen_width + right_pad, screen_height + top_pad))
    pygame.display.set_caption("Labyrinth Generator")
    terminate = False
    lab = Labyrinth(width, height)
    block = screen_width // width
    lab.set_visual_p(screen, block, top_pad)
    font = pygame.font.Font(None, 30)

    create_grid(screen, screen_width, screen_height, width, height, top_pad)

    pygame.display.flip()
    clock = pygame.time.Clock()
    start_settings = False
    while not terminate:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = int((event.pos[0]) // block)
                y = int((event.pos[1] - top_pad) // block)
                lab.path(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lab.reset()
                    create_grid(screen, screen_width, screen_height, width, height)
                    pygame.display.flip()

            pygame.display.flip()


main(60, 40)