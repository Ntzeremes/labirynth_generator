import random
import pygame
import copy
import time

pygame.init()


class Node:
    """A node is a part of the path. Each node is connected with the previous one, called parent.
    All the nodes connected create the path"""

    propagate_chance = 0.5
    parents_direction = 0.65

    def __init__(self, parent, pos):
        self.parent = parent
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def can_insert(self, width, height, grid):
        n = 0
        for i in range(2):
            for j in range(2):
                x = self.pos_x + i * (-1) ** j
                y = self.pos_y + (1 - i) * (-1) ** j
                if 0 <= x < width and 0 <= y < height:
                    if grid[y][x] is not None:
                        n += 1
        return True if n == 1 else False

    def neighbors(self, labyrinth):
        """checking the grid positions on the top, bottom, left and right of the Node.
        The parent node is excluded."""

        neighbors = []

        # Adding neighbors that are on top, bottom , right and left in the labyrinth
        # and we have not visited them so far.

        # top
        if self.pos_y - 1 >= 0:
            if labyrinth.grid[self.pos_y - 1][self.pos_x] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + i * (-1) ** j
                        y = self.pos_y - 1 + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x, self.pos_y - 1))

        # bottom
        if self.pos_y + 1 < labyrinth.height:
            if labyrinth.grid[self.pos_y + 1][self.pos_x] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + i * (-1) ** j
                        y = self.pos_y + 1 + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x, self.pos_y + 1))

        # left
        if self.pos_x - 1 >= 0:
            if labyrinth.grid[self.pos_y][self.pos_x - 1] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x - 1 + i * (-1) ** j
                        y = self.pos_y + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x - 1, self.pos_y))

        # right
        if self.pos_x + 1 < labyrinth.width:
            if labyrinth.grid[self.pos_y][self.pos_x + 1] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + 1 + i * (-1) ** j
                        y = self.pos_y + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x + 1, self.pos_y))
        return neighbors

    def children(self, lab):
        """choosing the child node of the current node"""
        neighbors = self.neighbors(lab)

        if not neighbors:
            return None
        second_child = None

        # Giving the same direction coming from parent a higher chance
        if self.parent:

            i = random.random()
            # keep parent's direction,it has a higher chance
            parents_direction_node = (2 * self.pos_x - self.parent[0], 2 * self.pos_y - self.parent[1])
            if parents_direction_node in neighbors:
                if len(neighbors) == 1 or i < Node.parents_direction:
                    first_child = Node((self.pos_x, self.pos_y), parents_direction_node)
                # else choose randomly between the other neighbors
                else:
                    neighbors.remove(parents_direction_node)
                    first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))
            else:
                first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))
        else:
            first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))

        l = len(neighbors)

        if l == 0:
            return None
        elif l > 1:
            propagate = random.random()
            if propagate < Node.propagate_chance :
                neighbors.remove((first_child.pos_x, first_child.pos_y))
                second_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))

        if second_child:
            return [first_child, second_child]

        return [first_child]


class Labyrinth:
    """The class that creates the n x n grid of the labyrinth. Initially it is filled with None values, the path
    is represented by values 0. Also has some basic functions for extra utility and manipulation and the function that
    creates the path."""

    def __init__(self, width, height):
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.screen = None
        self.block = None

    # noinspection PyTypeChecker
    def insert(self, x, y):
        """inserts a node in grid and prints it"""
        self.grid[y][x] = 0
        if self.screen:
            pygame.draw.rect(self.screen, (150, 150, 150),
                             (x * self.block + 1, y * self.block + 1, self.block - 1, self.block - 1))
            pygame.display.flip()

    def reset(self):
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self):
        for i in range(self.height):
            print(self.grid[i])
            print()

    def set_visual_p(self, screen, block):
        self.screen = screen
        self.block = block

    def path(self, x, y):
        """This function generates a random path inside the grid.
        The path starts at a random point at the edge of a grid and has fixed length"""

        # Choosing starting point at the edge of the grid. Corners are excluded
        current_nodes = [Node(None, (x, y))]
        self.insert(current_nodes[0].pos_x, current_nodes[0].pos_y)
        while current_nodes:
            current_node = current_nodes.pop(0)
            if current_node.can_insert(self.width, self.height, self.grid):
                self.insert(current_node.pos_x, current_node.pos_y)
            else:
                # Sometimes a child that was originally calculated can't be inserted cause of the other branches.
                child = current_node.children(self)
                if child:
                    current_node = random.choice(child)
                    if current_node.can_insert(self.width, self.height, self.grid):
                        self.insert(current_node.pos_x, current_node.pos_y)

            children = current_node.children(self)
            if children:
                current_nodes.extend(children)


def create_labyrinth(width, height):
    """Initializes and visualizes the creation of the path.
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


create_labyrinth(30, 20)

