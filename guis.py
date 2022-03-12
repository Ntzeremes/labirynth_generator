import pygame


class Text:
    """Text class that prints text on the screen surface"""

    def __init__(self, font, pos, width, height, text, text_color=(255, 255, 255), top_color=(0, 0, 0)):
        self.font = font
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.text = text
        self.text_color = text_color

        self.text_surf = font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(self.text_surf, self.text_rect)


class Changing_Text(Text):
    def change_text(self, text):
        self.text = text


class Text_Collection:
    """Collection of text objects so that with one draw call, all texts in the collection can be drawn"""
    def __init__(self, texts):
        self.texts = texts

    def draw(self, screen):
        for text in self.texts:
            text.draw(screen)


class Button:
    """Creates the buttons for gui"""

    def __init__(self, text, width, height, pos, font):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (160, 160, 160)
        self.pressed = False

        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(*mouse_pos):
            self.top_color = (220, 220, 220)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    return True
        else:
            self.top_color = (160, 160, 160)
        return False


# noinspection PyUnresolvedReferences
def starting_gui(screen, font, width, top_pad, right_pad):
    """Created the starting screen from which the user will choose the size of the labyrinth.

    Returns the grid size chosen by the user."""

    terminate = False
    clock = pygame.time.Clock()

    choice = None
    grid_choices = {0: [None, "9 x 6", (9, 6)], 1: [None, "15 x 12", (15, 12)], 2: [None, "30 x 20", (30, 20)],
                    3: [None, "60 x 40", (60, 40)]}
    text = "Choose the labyrinth grid size."
    page_text = Text(font, (100, 100), width - right_pad, 40, text)
    button_h = 90
    for i in range(len(grid_choices)):
        # noinspection PyTypeChecker
        grid_choices[i][0] = Button(grid_choices[i][1], 200, 50, (400, 210 + i * button_h), font)

    while not terminate:
        screen.fill((0, 0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        page_text.draw(screen)

        for i in range(len(grid_choices)):
            grid_choices[i][0].draw(screen)
            if grid_choices[i][0].check_click():
                choice = grid_choices[i][2]
                terminate = True

        pygame.display.flip()

    return choice


def lab_gui(font, width, height, top_pad, right_pad, d, p):
    horizontal_text = "space: restart labyrinth     R : reset the grid size"
    h_text = Text(font, (0, 0), width - 2 * right_pad, 50, horizontal_text, (0, 0, 0), (80, 80, 80))

    vertical_text1 = f" d:{d}"
    v_text1 = Changing_Text(font, (width + 1, 2 * top_pad), right_pad, 2 * top_pad, vertical_text1, (0, 0, 0), (80, 80, 80))
    vertical_text2 = f" p:{p}"
    v_text2 = Changing_Text(font, (width + 1, 7 * top_pad), right_pad, 2 * top_pad, vertical_text2, (0, 0, 0), (80, 80, 80))

    collection = Text_Collection([h_text, v_text1, v_text2])
    return collection


def draw_grid(screen, screen_width, screen_height, width, height, top_pad):
    """ Creates the height x width  grid of the labyrinth.
    Used when we start the program and every time we reset the labyrinth"""
    pygame.draw.rect(screen, (80, 80, 80), (0, top_pad, screen_width, screen_height))
    block = screen_width // width
    pygame.draw.line(screen, (0, 0, 0), (0, top_pad), (screen_width, top_pad))
    for i in range(height - 1):
        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1) * block + top_pad), (screen_width, (i + 1) * block + top_pad))
    for j in range(width):
        pygame.draw.line(screen, (0, 0, 0), ((j + 1) * block, top_pad), ((j + 1) * block, screen_height + top_pad))

