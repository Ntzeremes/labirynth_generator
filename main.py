import tkinter as tk
import pygame
from algorithm import *

pygame.init()


def settings():
    # Setting main widget
    root = tk.Tk()
    root.title("Game settings")
    root.geometry("480x600")
    root.configure(background="grey")

    grid = tk.Label(root, text="Grid size", font="ComicSans 24",
                     bg="grey").grid(row=2, column=0)

    # Lock window size
    root.update()
    root.minsize(480, 600)
    root.maxsize(480, 600)

    root.mainloop()


def create_labyrinth(width, height):
    """Initializes and visualizes the labyrinth using pygame and the classes from algorithm.py.
    """

    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((50, 50, 50))
    terminate = False
    lab = Labyrinth(width, height)

    # creating the grid
    block = screen_width // width
    for i in range(height - 1):
        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1) * block), (screen_width, (i + 1) * block))
    for j in range(width - 1):
        pygame.draw.line(screen, (0, 0, 0), ((j + 1) * block, 0), ((j + 1) * block, screen_height))

    lab.set_visual_p(screen, block)

    pygame.display.flip()
    clock = pygame.time.Clock()

    while not terminate:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = int((event.pos[0]) // block)
                y = int((event.pos[1]) // block)
                lab.path(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lab.reset()
                    screen.fill((50, 50, 50))
                    for i in range(height - 1):
                        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1) * block), (screen_width, (i + 1) * block))
                    for j in range(width - 1):
                        pygame.draw.line(screen, (0, 0, 0), ((j + 1) * block, 0), ((j + 1) * block, screen_height))
                    pygame.display.flip()

            pygame.display.flip()


settings()
