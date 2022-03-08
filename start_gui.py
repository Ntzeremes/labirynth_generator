import pygame


class Text:
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


def starting_gui(screen, font, width, top_pad, right_pad):
    terminate = False
    screen.fill((0, 0, 0))
    page = 1
    while not terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        if page == 1:

            grid_choices = {0: [None, "9 x 6"], 1: [None, "15 x 12"], 2: [None, "30 x 20"], 3: [None, "60 x 40"]}
            text = "The labyrinth has a 3:2  width to height ratio."
            textb = "Choose a grid size."
            page_text = Text(font, (500, 50), width - right_pad, 40, text)
            page_textb = Text(font, (500, 100), width - right_pad, 40, textb)
            page_text.draw(screen)
            page_textb.draw(screen)

            buttons = False
            button_h = 90

            if not buttons:
                for i in range(len(grid_choices)):
                    grid_choices[i][0] = Button(grid_choices[i][1], 200, 50, (400, 210 + i * button_h), font)

            for i in range(len(grid_choices)):
                grid_choices[i][0].draw(screen)

            pygame.display.flip()

        else:
            screen.fill((0, 0, 0))


