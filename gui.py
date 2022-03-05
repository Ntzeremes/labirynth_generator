import pygame


class Text:
    """Class that renders text on the screen"""
    def __init__(self, font, pos, width, height, text):
        self.font = font
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (255, 255, 255)
        self.text = text

    def draw(self):
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)


class Button:
    """Creates the buttons for gui"""
    def __init__(self, text, width, height, pos, font):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (200, 200, 200)
        self.pressed = False

        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.


def starting_gui(screen, font):
    page = 1

    if page ==1:
        grid_choices = {0: (9, 6), 1: (12, 8), 2: (30, 20), 3: (60, 40)}
        text = "The labyrinth has a 3:2  width to height ratio." \
               "Chose labyrinth size."

        page = 2

    else:

        return True
