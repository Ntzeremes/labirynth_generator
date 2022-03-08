import pygame


class Text:
    """Text class that prints text on the screen surface"""
    def __init__(self, font, pos, width, height, text):
        self.font = font
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (255, 255, 255)
        self.text = text

        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(self.text_surf, self.text_rect)


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
    """Created the starting screen from which the user will choose the size of the labyrinth"""
    terminate = False
    clock = pygame.time.Clock()

    choice = None
    grid_choices = {0: [None, "9 x 6", (9, 6)], 1: [None, "15 x 12", (15, 12)], 2: [None, "30 x 20", (30, 20)],
                    3: [None, "60 x 40", (60, 40)]}
    text = "Choose the labyrinth grid size."
    page_text = Text(font, (100, 100), width - right_pad, 40, text)
    button_h = 90
    for i in range(len(grid_choices)):
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
