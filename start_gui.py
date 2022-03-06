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
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(*mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    return True
        return False


def starting_gui(screen, font):
    page = 1

    if page == 1:
        screen.fill((0,0,0))
        grid_choices = {0: (9, 6), 1: (12, 8), 2: (30, 20), 3: (60, 40)}
        text = "The labyrinth has a 3:2  width to height ratio." \
               "Chose labyrinth size."

        info = Text()

        page = 2

    else:

        return True
